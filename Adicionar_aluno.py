#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import re
from datetime import date, datetime
from getpass import getpass

# ========= Configurações auxiliares =========

AGRO_CODES = ['AGRO1', 'AGRO2', 'AGRO3']
ALIM_CODES = ['ALIM1', 'ALIM2', 'ALIM3']
INFO_CODES = ['INFO1', 'INFO2', 'INFO3']

DEPARTS = [
    ('DEP-AGRO', 'Departamento de Agropecuária', '1130001001', 'dep.agro@escola.edu.br'),
    ('DEP-ALIM', 'Departamento de Alimentos',    '1130001002', 'dep.alim@escola.edu.br'),
    ('DEP-INF',  'Departamento de Informática',  '1130001003', 'dep.inf@escola.edu.br'),
]

PROFS = [
    ('PRF-AGRO', '11111111111', 'Ana Ribeiro',    'ana.ribeiro@escola.edu.br',  '11970010001', '1978-05-13', 'Mestre',       '2020-02-01', 'DEP-AGRO'),
    ('PRF-ALIM', '22222222222', 'Bruno Carvalho', 'bruno.carvalho@escola.edu.br','11970010002', '1982-09-21', 'Mestre',       '2019-03-01', 'DEP-ALIM'),
    ('PRF-INF',  '33333333333', 'Carla Nogueira', 'carla.nogueira@escola.edu.br','11970010003', '1985-12-02', 'Especialista', '2021-01-15', 'DEP-INF'),
]

COURSES = [
    ('TEC-AGRO', 'Técnico em Agropecuária', 'Técnico', 6, 1200, 'DEP-AGRO', 'PRF-AGRO', '2015-02-01', 'ativo'),
    ('TEC-ALIM', 'Técnico em Alimentos',    'Técnico', 6, 1200, 'DEP-ALIM', 'PRF-ALIM', '2016-02-01', 'ativo'),
    ('TEC-INF',  'Técnico em Informática',  'Técnico', 6, 1200, 'DEP-INF',  'PRF-INF',  '2017-02-01', 'ativo'),
]

# Mapeamento letra->curso e ano->disciplina
COURSE_BY_LETTER = {
    'A': 'TEC-AGRO', 'B': 'TEC-AGRO', 'C': 'TEC-AGRO', 'D': 'TEC-AGRO',
    'E': 'TEC-ALIM',
    'F': 'TEC-INF',  'G': 'TEC-INF',
}

DISC_CODE_BY = {
    ('TEC-AGRO', 1): 'AGRO1',
    ('TEC-AGRO', 2): 'AGRO2',
    ('TEC-AGRO', 3): 'AGRO3',
    ('TEC-ALIM', 1): 'ALIM1',
    ('TEC-ALIM', 2): 'ALIM2',
    ('TEC-ALIM', 3): 'ALIM3',
    ('TEC-INF',  1): 'INFO1',
    ('TEC-INF',  2): 'INFO2',
    ('TEC-INF',  3): 'INFO3',
}

# ========= Funções utilitárias =========
def ask(prompt, default=None, validator=None, required=True):
    while True:
        val = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
        if not val and default is not None:
            val = default
        if not val and required:
            print("Valor obrigatório.")
            continue
        if validator and val:
            ok, msg = validator(val)
            if not ok:
                print(f"Inválido: {msg}")
                continue
        return val

def validate_year_serial(m):
    if not re.fullmatch(r"\d{5,}", m):
        return False, "Use apenas dígitos, mínimo 5 (AAAA + serial)."
    year = int(m[:4])
    if year < 1990 or year > 2100:
        return False, "Ano (4 primeiros dígitos) fora do intervalo 1990–2100."
    return True, ""

def validate_digits(n, length=None):
    if not re.fullmatch(r"\d+", n):
        return False, "Use apenas dígitos."
    if length and len(n) != length:
        return False, f"Use exatamente {length} dígitos."
    return True, ""

def validate_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Use o formato AAAA-MM-DD."

def validate_estado(s):
    return (len(s) == 2 and s.isalpha()), "UF deve ter 2 letras."

def validate_turma(code):
    if not re.fullmatch(r"[123][A-G]", code.upper()):
        return False, "Formato inválido. Use, por exemplo, 1A, 2G, 3E."
    return True, ""

# ========= Acesso ao banco =========

def get_conn():
    host = ask("Host do banco", "localhost")
    port = int(ask("Porta", "5432", validator=lambda v: (v.isdigit(), "Porta deve ser numérica.")))
    db   = ask("Database", "escola")
    user = ask("Usuário", "postgres")
    pwd  = getpass("Senha: ")
    dsn = f"host={host} port={port} dbname={db} user={user} password={pwd}"
    return psycopg2.connect(dsn)

def fetchone(cur, q, params=None):
    cur.execute(q, params or ())
    return cur.fetchone()

def fetchval(cur, q, params=None):
    row = fetchone(cur, q, params)
    return row[0] if row else None

# ========= Seed de dados-base =========

def ensure_departments(cur):
    ids = {}
    for codigo, nome, tel, email in DEPARTS:
        id_dep = fetchval(cur, "SELECT id_departamento FROM departamentos WHERE codigo=%s", (codigo,))
        if not id_dep:
            cur.execute("""
                INSERT INTO departamentos (codigo, nome, telefone, email)
                VALUES (%s, %s, %s, %s)
                RETURNING id_departamento
            """, (codigo, nome, tel, email))
            id_dep = cur.fetchone()[0]
        ids[codigo] = id_dep
    return ids

def ensure_professors(cur, dep_ids):
    ids = {}
    for matricula, cpf, nome, email, tel, data_nasc, titulacao, data_contrat, dep_code in PROFS:
        id_prof = fetchval(cur, "SELECT id_professor FROM professores WHERE matricula=%s", (matricula,))
        if not id_prof:
            cur.execute("""
                INSERT INTO professores
                (matricula, cpf, nome_completo, email, telefone, data_nascimento,
                 titulacao, data_contratacao, departamento_id, status_professor)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'ativo')
                RETURNING id_professor
            """, (matricula, cpf, nome, email, tel, data_nasc, titulacao, data_contrat, dep_ids[dep_code]))
            id_prof = cur.fetchone()[0]
        ids[matricula] = id_prof
    return ids

def ensure_courses(cur, dep_ids, prof_ids):
    ids = {}
    for codigo, nome, grau, duracao, ch_total, dep_code, coord_mat, data_criacao, status in COURSES:
        id_curso = fetchval(cur, "SELECT id_curso FROM cursos WHERE codigo=%s", (codigo,))
        if not id_curso:
            cur.execute("""
                INSERT INTO cursos
                (codigo, nome, grau, duracao_semestres, carga_horaria_total,
                 departamento_id, coordenador_id, data_criacao, status_curso)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_curso
            """, (codigo, nome, grau, duracao, ch_total,
                  dep_ids[dep_code], prof_ids[coord_mat], data_criacao, status))
            id_curso = cur.fetchone()[0]
        ids[codigo] = id_curso
    return ids

def ensure_periodo_letivo(cur, ano, semestre, status='em_andamento'):
    id_periodo = fetchval(cur, "SELECT id_periodo FROM periodos_letivos WHERE ano=%s AND semestre=%s", (ano, semestre))
    if not id_periodo:
        cur.execute("""
            INSERT INTO periodos_letivos
            (ano, semestre, data_inicio, data_fim, data_inicio_matriculas, data_fim_matriculas, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_periodo
        """, (ano, semestre, f"{ano}-08-01", f"{ano}-12-20", f"{ano}-07-10", f"{ano}-08-10", status))
        id_periodo = cur.fetchone()[0]
    return id_periodo

def ensure_disciplinas(cur, dep_ids):
    mapa = {}
    base = [
        ('AGRO1','Agropecuária I',   60,4,'Bases de agropecuária','Refs', 'DEP-AGRO','obrigatoria'),
        ('AGRO2','Agropecuária II',  60,4,'Sist. produção vegetal','Refs','DEP-AGRO','obrigatoria'),
        ('AGRO3','Agropecuária III', 60,4,'Sist. produção animal','Refs','DEP-AGRO','obrigatoria'),
        ('ALIM1','Alimentos I',      60,4,'Introd. tecnologia','Refs','DEP-ALIM','obrigatoria'),
        ('ALIM2','Alimentos II',     60,4,'Processos e conservação','Refs','DEP-ALIM','obrigatoria'),
        ('ALIM3','Alimentos III',    60,4,'Controle de qualidade','Refs','DEP-ALIM','obrigatoria'),
        ('INFO1','Informática I',    60,4,'Lógica e fundamentos','Refs','DEP-INF','obrigatoria'),
        ('INFO2','Informática II',   60,4,'EDs e web','Refs','DEP-INF','obrigatoria'),
        ('INFO3','Informática III',  60,4,'Redes e desenvolvimento','Refs','DEP-INF','obrigatoria'),
    ]
    for codigo, nome, ch, cred, ementa, biblio, dep_code, tipo in base:
        id_disc = fetchval(cur, "SELECT id_disciplina FROM disciplinas WHERE codigo=%s", (codigo,))
        if not id_disc:
            cur.execute("""
                INSERT INTO disciplinas
                (codigo, nome, carga_horaria, creditos, ementa, bibliografia, departamento_id, tipo)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_disciplina
            """, (codigo, nome, ch, cred, ementa, biblio, dep_ids[dep_code], tipo))
            id_disc = cur.fetchone()[0]
        mapa[codigo] = id_disc
    return mapa

def ensure_turmas(cur, id_periodo, prof_ids, disc_ids):
    # Gera 21 turmas: 1A..3G
    def turma_info(code):
        ano = int(code[0])
        letra = code[1]
        curso = COURSE_BY_LETTER[letra]
        disc_code = DISC_CODE_BY[(curso, ano)]
        if curso == 'TEC-AGRO':
            prof = 'PRF-AGRO'
        elif curso == 'TEC-ALIM':
            prof = 'PRF-ALIM'
        else:
            prof = 'PRF-INF'
        return disc_code, prof

    created = {}
    for ano in (1,2,3):
        for letra in ('A','B','C','D','E','F','G'):
            code = f"{ano}{letra}"
            disc_code, prof_code = turma_info(code)
            id_turma = fetchval(cur, "SELECT id_turma FROM turmas WHERE codigo=%s AND periodo_letivo_id=%s", (code, id_periodo))
            if not id_turma:
                cur.execute("""
                    INSERT INTO turmas
                    (codigo, disciplina_id, periodo_letivo_id, professor_id, vagas_total, horario, sala, dias_semana, status_turma)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id_turma
                """, (code, disc_ids[disc_code], id_periodo, prof_ids[prof_code],
                      40, '08:00-10:00', f"SALA {letra}{ano}", 'Seg,Qua', 'aberta'))
                id_turma = cur.fetchone()[0]
            created[code] = id_turma
    return created

def guess_email(nome, idx):
    base = re.sub(r"[^a-zA-Z0-9]+", ".", nome.strip().lower()).strip(".")
    return f"{base}.{idx:03d}@alunos.escola.edu.br"

# ========= Fluxo principal =========

def main():
    print("Cadastro interativo de 21 alunos com criação de 7 turmas (1A..3G) e vínculos necessários.")
    conn = get_conn()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            ano = int(ask("Ano do período letivo", "2025", validator=lambda v: (v.isdigit(), "Ano numérico")))
            semestre = int(ask("Semestre do período letivo (1 ou 2)", "2", validator=lambda v: (v in ("1","2"), "Use 1 ou 2")))
            print("Garantindo cadastros-base...")
            dep_ids = ensure_departments(cur)
            prof_ids = ensure_professors(cur, dep_ids)
            course_ids = ensure_courses(cur, dep_ids, prof_ids)
            id_periodo = ensure_periodo_letivo(cur, ano, semestre)
            disc_ids = ensure_disciplinas(cur, dep_ids)
            turma_ids = ensure_turmas(cur, id_periodo, prof_ids, disc_ids)
            conn.commit()
            print("Base pronta.\n")

        qtd = int(ask("Quantos alunos cadastrar", "21", validator=lambda v: (v.isdigit() and int(v)>0, "Informe um inteiro > 0")))
        idx_email = 1

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            for i in range(qtd):
                print(f"\nAluno {i+1}/{qtd}")
                nome = ask("Nome completo")
                matricula = ask("Matrícula (AAAA + SERIAL numérico)", validator=validate_year_serial)
                cpf = ask("CPF (11 dígitos)", validator=lambda v: validate_digits(v, 11))
                email = ask("E-mail (enter para sugerir)", default="")
                if not email:
                    email = guess_email(nome, idx_email)
                    idx_email += 1
                telefone = ask("Telefone", default="11980010000", validator=lambda v: (True, ""))
                data_nascimento = ask("Data de nascimento (AAAA-MM-DD)", '2007-01-01', validator=validate_date)
                endereco = ask("Endereço", default="Rua Exemplo, 100")
                cidade = ask("Cidade", default="São Paulo")
                estado = ask("UF (2 letras)", "SP", validator=validate_estado)
                cep = ask("CEP (8 dígitos)", "01000000", validator=lambda v: validate_digits(v, 8))
                ano_matricula = int(matricula[:4])
                data_ingresso = ask("Data de ingresso (AAAA-MM-DD)", f"{ano_matricula}-02-01", validator=validate_date)
                turma_code = ask("Turma (ex.: 1A, 2G, 3E)", validator=validate_turma).upper()

                # Inserir aluno
                try:
                    cur.execute("""
                        INSERT INTO alunos
                        (matricula, cpf, nome_completo, email, telefone, data_nascimento,
                         endereco, cidade, estado, cep, data_ingresso, status_aluno)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'ativo')
                        RETURNING id_aluno
                    """, (matricula, cpf, nome, email, telefone, data_nascimento,
                          endereco, cidade, estado, cep, data_ingresso))
                    id_aluno = cur.fetchone()[0]
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    raise
                except Exception:
                    conn.rollback()
                    raise

                # Vincular ao curso
                letra = turma_code[1]
                curso_code = COURSE_BY_LETTER[letra]
                id_curso = course_ids[curso_code]
                forma_ingresso = ask("Forma de ingresso", "processo_seletivo")
                cur.execute("""
                    INSERT INTO matriculas_curso
                    (aluno_id, curso_id, data_matricula, periodo_ingresso, forma_ingresso)
                    VALUES (%s,%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (id_aluno, id_curso, f"{ano_matricula}-02-10", f"{ano_matricula}/1", forma_ingresso))

                # Vincular à turma
                id_turma = turma_ids.get(turma_code)
                if not id_turma:
                    raise RuntimeError(f"Turma {turma_code} não localizada para o período.")
                cur.execute("""
                    INSERT INTO matriculas_turma (aluno_id, turma_id, data_matricula)
                    VALUES (%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (id_aluno, id_turma, f"{ano}-{semestre}-02-20".replace("-1-","-02-").replace("-2-","-02-")))

                conn.commit()
                print(f"Aluno cadastrado e vinculado: {nome} → {turma_code} ({curso_code}).")

        print("\nConcluído com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Falha:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
