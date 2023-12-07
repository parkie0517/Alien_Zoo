from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

# DB 생성 및 연결에 필요한 Connection을 반환하는 함수
def get_db_connection():
    conn = sqlite3.connect('alien_zoo.db', check_same_thread=False)
    conn.row_factory=sqlite3.Row
    return conn

# 테이블을 생성하는 함수
def create_table():
    conn = get_db_connection()

    # User 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS user
    (
    money INTEGER NOT NULL
    )
    """
    )

    # Galaxy 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS galaxy
    (
    galaxyname VARCHAR(20) PRIMARY KEY,
    description VARCHAR(40) NOT NULL
    )
    """
    )

    # Planet 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS planet
    (
    planetid INTEGER PRIMARY KEY,
    galaxyname VARCHAR(20) NOT NULL,
    planetname VARCHAR(20) NOT NULL,
    FOREIGN KEY (galaxyname) REFERENCES galaxy(galaxyname)
    )
    """
    )

    # Alien 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS alien
    (
    alienid INTEGER PRIMARY KEY,
    planetid INTEGER NOT NULL,
    alienname VARCHAR(20) NOT NULL,
    ability VARCHAR(20),
    clue VARCHAR(2),
    FOREIGN KEY (planetid) REFERENCES planet(planetid)
    )
    """
    )

    # Explorer 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS explorer
    (
    explorerid INTEGER PRIMARY KEY AUTOINCREMENT,
    explorername VARCHAR(20) NOT NULL,
    cost INTEGER NOT NULL,
    major VARCHAR(20),
    employed INTEGER DEFAULT 0 CHECK (employed IN (0, 1)) NOT NULL
    )
    """
    )

    # Pilot 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS pilot
    (
    pilotid INTEGER PRIMARY KEY AUTOINCREMENT,
    pilotname VARCHAR(20) NOT NULL,
    cost INTEGER NOT NULL,
    level INTEGER CHECK (level IN (1, 2)) NOT NULL,
    employed INTEGER DEFAULT 0 CHECK (employed IN (0, 1)) NOT NULL
    )
    """
    )

    # History 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS history
    (
    expeditionnumber INTEGER PRIMARY KEY AUTOINCREMENT,
    planetid INTEGER NOT NULL,
    explorerid1 INTEGER NOT NULL,
    explorerid2 INTEGER NOT NULL,
    pilotid INTEGER NOT NULL,
    alienid INTEGER NOT NULL,
    success INTEGER CHECK (success IN (0, 1)) NOT NULL,
    FOREIGN KEY (planetid) REFERENCES planet(planetid),
    FOREIGN KEY (explorerid1) REFERENCES explorer(explorerid),
    FOREIGN KEY (explorerid2) REFERENCES explorer(explorerid),
    FOREIGN KEY (pilotid) REFERENCES pilot(pilotid),
    FOREIGN KEY (alienid) REFERENCES alien(alienid)
    )
    """
    )

    # Zoo 테이블 생성하기
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS zoo
    (
    alienid INTEGER PRIMARY KEY,
    expeditionnumber INTEGER NOT NULL,
    FOREIGN KEY (alienid) REFERENCES alien(alienid),
    FOREIGN KEY (expeditionnumber) REFERENCES history(expeditionnumber)
    )
    """
    )

    conn.close()

# 테이블에 초기 데이터를 삽입하는 함수
def insert_data():
    conn = get_db_connection()

    # User 테이블에 데이터 삽입
    conn.execute("INSERT INTO user (money) VALUES (10000)")

    # Galaxy 테이블에 데이터 삽입
    conn.execute("INSERT INTO galaxy (galaxyname, description) VALUES ('물 은하', '물의 은하는 물로 뒤덮인 행성들로 구성되어 있습니다.')")
    conn.execute("INSERT INTO galaxy (galaxyname, description) VALUES ('불 은하', '불의 은하는 마그마로 뒤덮인 행성들로 구성되어 있습니다.')")
    conn.execute("INSERT INTO galaxy (galaxyname, description) VALUES ('흙 은하', '흙의 은하는 산으로 뒤덮인 행성들로 구성되어 있습니다.')")
    conn.execute("INSERT INTO galaxy (galaxyname, description) VALUES ('비밀 은하', '전설에만 존재한다는 비밀 은하입니다.')")
        
    # Planet 테이블에 데이터 삽입
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('11', '물 은하', '수소성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('12', '물 은하', '수중성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('13', '물 은하', '수대성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('14', '물 은하', '수비성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('21', '불 은하', '화소성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('22', '불 은하', '화중성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('23', '불 은하', '화대성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('24', '불 은하', '화비성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('31', '흙 은하', '토소성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('32', '흙 은하', '토중성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('33', '흙 은하', '토대성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('34', '흙 은하', '토비성')")
    conn.execute("INSERT INTO planet (planetid, galaxyname, planetname) VALUES ('40', '비밀 은하', '신비성')")
    
    # Alien 테이블에 데이터 삽입
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (11, 11, '물의 요정', NULL, '3')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (12, 12, '물귀신', NULL, '4')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (13, 13, '물 먹는 하마', NULL, '5')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (14, 14, '포세이돈', '해일', '99')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (21, 21, '불나방', NULL, '5')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (22, 22, '불사조', NULL, '41')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (23, 23, '불드래곤', NULL, '8')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (24, 24, '발록', '화산', '5')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (31, 31, '흙박쥐', NULL, '12')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (32, 32, '짱동 마스터', NULL, '3')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (33, 33, '흙고래', NULL, '4')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (34, 34, '돌하르방', '지진', '17')")
    conn.execute("INSERT INTO alien (alienid, planetid, alienname, ability, clue) VALUES (40, 40, '그로구', NULL, NULL)")
    
    # Explorer 테이블에 데이터 삽입
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('인디아나 존슨', 500, NULL)")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('헬 보이', 1000, '화산')")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('간달프', 600, NULL)")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('두더지 선생', 950, '지진')")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('이순신 장군', 2100, '해일')")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('스티븐 제라드', 820, NULL)")
    conn.execute("INSERT INTO explorer (explorername, cost, major) VALUES ('김병만', 10, NULL)")

    # Pilot 테이블에 데이터 삽입
    conn.execute("INSERT INTO pilot (pilotname, cost, level) VALUES ('톰 크루즈', 3200, 2)")
    conn.execute("INSERT INTO pilot (pilotname, cost, level) VALUES ('닐 암스트롱', 500, 1)")
    conn.execute("INSERT INTO pilot (pilotname, cost, level) VALUES ('라이트 형제', 100, 1)")
    conn.execute("INSERT INTO pilot (pilotname, cost, level) VALUES ('자전차왕 엄복동', 20, 1)")
    conn.execute("INSERT INTO pilot (pilotname, cost, level) VALUES ('베이비 드라이버', 400, 2)")
    
    conn.commit()
    conn.close()

""" (교수님께서 실행할 때는 초기 세팅진행을 안 하셔도 됩니다.)
게임 시작 전 초기 4 Step 초기 세팅
step1: 만약 DB 폴더 안에 alien_zoo.db가 존재한다면 삭제하기
step2: 196줄 주석 해제하고 실행
step3: 196줄 주석 처리하고, 197줄 주석 해제하고 실행
step4: 196줄, 197줄 모두 주석처리하고 게임 실행
"""
# create_table()
# insert_data()
app = Flask(__name__)
app.secret_key = 'parkie0517'  # 보안을 위한 Secret Key

# 시작 페이지 
@app.route('/')
def index():
    return render_template('page_1_1.html')

# 시나리오 설명 페이지
@app.route('/page_1_2')
def page_1_2():
    return render_template('page_1_2.html')

# 게임 목표 설명 페이지
@app.route('/page_1_3')
def page_1_3():
    return render_template('page_1_3.html')

# Main 페이지
@app.route('/page_2')
def page_2():
    conn = get_db_connection()
    cursor = conn.cursor()

    # User 테이블에서 돈 갖고 오기
    cursor.execute("SELECT money FROM user")
    money = cursor.fetchone()

    # Zoo 테이블에서 데이터 가져오기
    cursor.execute("SELECT alienid, alienname FROM alien WHERE alienid IN (SELECT alienid FROM ZOO)")
    # cursor.execute("SELECT alienid FROM ZOO")
    # cursor.execute("SELECT alienid, alienname FROM alien")
    zoo_data = cursor.fetchall()

    cursor.close()
    conn.close()

    alien_1_1 = ""
    alien_1_2 = ""
    alien_1_3 = ""
    alien_1_4 = ""
    alien_2_1 = ""
    alien_2_2 = ""
    alien_2_3 = ""
    alien_2_4 = ""
    alien_3_1 = ""
    alien_3_2 = ""
    alien_3_3 = ""
    alien_3_4 = ""
    
    for i, value in enumerate(zoo_data):
        if value[0] == 11:
            alien_1_1 = value[1]
        elif value[0] == 12:
            alien_1_2 = value[1]
        elif value[0] == 13:
            alien_1_3 = value[1]
        elif value[0] == 14:
            alien_1_4 = value[1]
        elif value[0] == 21:
            alien_2_1 = value[1]
        elif value[0] == 22:
            alien_2_2 = value[1]
        elif value[0] == 23:
            alien_2_3 = value[1]
        elif value[0] == 24:
            alien_2_4 = value[1]
        elif value[0] == 31:
            alien_3_1 = value[1]
        elif value[0] == 32:
            alien_3_2 = value[1]
        elif value[0] == 33:
            alien_3_3 = value[1]
        elif value[0] == 34:
            alien_3_4 = value[1]

    return render_template('page_2.html',
                           money = money[0],
                           alien_1_1 = alien_1_1, alien_1_2 = alien_1_2, alien_1_3 = alien_1_3, alien_1_4 = alien_1_4,
                           alien_2_1 = alien_2_1, alien_2_2 = alien_2_2, alien_2_3 = alien_2_3, alien_2_4 = alien_2_4,
                           alien_3_1 = alien_3_1, alien_3_2 = alien_3_2, alien_3_3 = alien_3_3, alien_3_4 = alien_3_4
                           )

# 탐험대 고용 페이지
@app.route('/page_3')
def page_3():
    conn = get_db_connection()
    cursor = conn.cursor()

    # User 테이블에서 돈 갖고 오기
    cursor.execute("SELECT money FROM user")
    money = cursor.fetchone()

    # 아직 고용이 안된 Explorer 테이블 가져오기
    cursor.execute("SELECT * FROM explorer WHERE employed = 0")
    explorer_data = cursor.fetchall()

    # 아직 고용이 안된 Pilot 테이블 가져오기
    cursor.execute("SELECT * FROM pilot WHERE employed = 0")
    pilot_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('page_3.html',
                           money = money[0],
                           explorer_data = explorer_data,
                           pilot_data = pilot_data
                           )

# Explorer를 사는 데 필요한 함수
@app.route('/buy_explorer', methods=['POST'])
def buy_explorer():
    n = request.form.get('n')
    n = int(n)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 현재 보유한 돈 가져오기
    cursor.execute("SELECT money FROM user")
    money = cursor.fetchone()
    money = money[0]

    # 고용하려는 탐험대의 가격 검색하기
    cursor.execute("SELECT cost FROM explorer WHERE explorerid = ?", (n,))
    cost = cursor.fetchone()
    cost = cost[0]

    # 구매 가능 여부 확인하기
    if money >= cost:
        cursor.execute("UPDATE explorer SET employed = 1 WHERE explorerid = ?", (n,)) # 고용 상태 변경하기
        cursor.execute("UPDATE user SET money = ?", (money - cost,)) # 돈 차감하기
        conn.commit()
        
    cursor.close()
    conn.close()

    return redirect(url_for('page_3'))

# Pilot을 사는 데 필요한 함수 (위 함수와 작동 방식이 동일해서 주석은 생략함)
@app.route('/buy_pilot', methods=['POST'])
def buy_pilot():
    n = request.form.get('n')
    n = int(n)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT money FROM user")
    money = cursor.fetchone()
    money = money[0]

    cursor.execute("SELECT cost FROM pilot WHERE pilotid = ?", (n,))
    cost = cursor.fetchone()
    cost = cost[0]

    if money >= cost:
        cursor.execute("UPDATE pilot SET employed = 1 WHERE pilotid = ?", (n,))
        cursor.execute("UPDATE user SET money = ?", (money - cost,))
        conn.commit()
        
    cursor.close()
    conn.close()

    return redirect(url_for('page_3'))

# 연구소 페이지
@app.route('/page_4')
def page_4():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Zoo 테이블에서 데이터 가져오기
    cursor.execute("SELECT alienid, alienname, clue FROM alien WHERE alienid IN (SELECT alienid FROM ZOO)")
    zoo_data = cursor.fetchall()

    alien_1_1 = ""
    alien_1_2 = ""
    alien_1_3 = ""
    alien_1_4 = ""
    alien_2_1 = ""
    alien_2_2 = ""
    alien_2_3 = ""
    alien_2_4 = ""
    alien_3_1 = ""
    alien_3_2 = ""
    alien_3_3 = ""
    alien_3_4 = ""
    
    alien_1_1_dna = ""
    alien_1_2_dna = ""
    alien_1_3_dna = ""
    alien_1_4_dna = ""
    alien_2_1_dna = ""
    alien_2_2_dna = ""
    alien_2_3_dna = ""
    alien_2_4_dna = ""
    alien_3_1_dna = ""
    alien_3_2_dna = ""
    alien_3_3_dna = ""
    alien_3_4_dna = ""

    for i, value in enumerate(zoo_data):
        if value[0] == 11:
            alien_1_1 = value[1]
            alien_1_1_dna = value[2]
        elif value[0] == 12:
            alien_1_2 = value[1]
            alien_1_2_dna = value[2]
        elif value[0] == 13:
            alien_1_3 = value[1]
            alien_1_3_dna = value[2]
        elif value[0] == 14:
            alien_1_4 = value[1]
            alien_1_4_dna = value[2]
        elif value[0] == 21:
            alien_2_1 = value[1]
            alien_2_1_dna = value[2]
        elif value[0] == 22:
            alien_2_2 = value[1]
            alien_2_2_dna = value[2]
        elif value[0] == 23:
            alien_2_3 = value[1]
            alien_2_3_dna = value[2]
        elif value[0] == 24:
            alien_2_4 = value[1]
            alien_2_4_dna = value[2]
        elif value[0] == 31:
            alien_3_1 = value[1]
            alien_3_1_dna = value[2]
        elif value[0] == 32:
            alien_3_2 = value[1]
            alien_3_2_dna = value[2]
        elif value[0] == 33:
            alien_3_3 = value[1]
            alien_3_3_dna = value[2]
        elif value[0] == 34:
            alien_3_4 = value[1]
            alien_3_4_dna = value[2]

    cursor.close()
    conn.close()

    return render_template('page_4.html',
                           alien_1_1 = alien_1_1, alien_1_2 = alien_1_2, alien_1_3 = alien_1_3, alien_1_4 = alien_1_4,
                           alien_2_1 = alien_2_1, alien_2_2 = alien_2_2, alien_2_3 = alien_2_3, alien_2_4 = alien_2_4,
                           alien_3_1 = alien_3_1, alien_3_2 = alien_3_2, alien_3_3 = alien_3_3, alien_3_4 = alien_3_4,
                           alien_1_1_dna = alien_1_1_dna, alien_1_2_dna = alien_1_2_dna, alien_1_3_dna = alien_1_3_dna, alien_1_4_dna = alien_1_4_dna,
                           alien_2_1_dna = alien_2_1_dna, alien_2_2_dna = alien_2_2_dna, alien_2_3_dna = alien_2_3_dna, alien_2_4_dna = alien_2_4_dna,
                           alien_3_1_dna = alien_3_1_dna, alien_3_2_dna = alien_3_2_dna, alien_3_3_dna = alien_3_3_dna, alien_3_4_dna = alien_3_4_dna
                           )

# 탐험대 구성 페이지
@app.route('/page_5_1')
def page_5_1():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 고용된 Explorer 테이블 가져오기
    cursor.execute("SELECT * FROM explorer WHERE employed = 1")
    explorer_data = cursor.fetchall()

    # 고용된 Pilot 테이블 가져오기
    cursor.execute("SELECT * FROM pilot WHERE employed = 1")
    pilot_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('page_5_1.html',
                           explorer_data = explorer_data,
                           pilot_data = pilot_data
                           )

# 탐험대 조합 생성 함수
@app.route('/build_team', methods=['POST'])
def build_team():
    # Session 변수를 사용해서 대원들 ID값을 저장하기
    explorerid1 = request.form.get('e1')
    explorerid2 = request.form.get('e2')
    pilotid = request.form.get('p1')
    team_info = [explorerid1, explorerid2, pilotid]
    session['team_info'] = team_info

    return redirect(url_for('page_5_2'))

# 은하 목록 페이지
@app.route('/page_5_2')
def page_5_2():
    return render_template('page_5_2.html')

# Boss 행성 탐험을 위한 좌표 처리
@app.route('/process_coordinates', methods=['POST'])
def process_coordinates():
    x = request.form.get('x')
    y = request.form.get('y')
    z = request.form.get('z')

    if x == "3" and y == "4" and z == "5":
        return render_template('page_8_1_4.html') # 물 Boss Planet
    elif x == "5" and y == "41" and z == "8":
        return render_template('page_8_2_4.html') # 불 Boss Planet
    elif x == "12" and y == "3" and z == "4":
        return render_template('page_8_3_4.html') # 흙 Boss Planet
    elif x == "99" and y == "5" and z == "17":
        return render_template('page_8_4.html') # 최종 Boss Planet
    else:
        return render_template('page_5_2.html') # 존재하지 않는 행성의 좌표를 입력했을 경우

# 물 은하 행성 목록 페이지
@app.route('/page_6_1')
def page_6_1():
    return render_template('page_6_1.html')

# 불 은하 행성 목록 페이지
@app.route('/page_6_2')
def page_6_2():
    return render_template('page_6_2.html')

# 흙 은하 행성 목록 페이지
@app.route('/page_6_3')
def page_6_3():
    return render_template('page_6_3.html')

# 물 은하 Small 행성
@app.route('/page_8_1_1')
def page_8_1_1():
    return render_template('page_8_1_1.html')

# 물 은하 Large 행성
@app.route('/page_8_1_2')
def page_8_1_2():
    return render_template('page_8_1_2.html')

# 물 은하 Huge 행성
@app.route('/page_8_1_3')
def page_8_1_3():
    return render_template('page_8_1_3.html')

# 불 은하 Small 행성
@app.route('/page_8_2_1')
def page_8_2_1():
    return render_template('page_8_2_1.html')

# 불 은하 Large 행성
@app.route('/page_8_2_2')
def page_8_2_2():
    return render_template('page_8_2_2.html')

# 불 은하 Huge 행성
@app.route('/page_8_2_3')
def page_8_2_3():
    return render_template('page_8_2_3.html')

# 흙 은하 Small 행성
@app.route('/page_8_3_1')
def page_8_3_1():
    return render_template('page_8_3_1.html')

# 흙 은하 Large 행성
@app.route('/page_8_3_2')
def page_8_3_2():
    return render_template('page_8_3_2.html')

# 흙 은하 Huge 행성
@app.route('/page_8_3_3')
def page_8_3_3():
    return render_template('page_8_3_3.html')

# Alien 포획 기능
@app.route('/capture_alien', methods=['POST'])
def capture_alien():
    if '11' in request.form:
        alienid = 11
    elif '12' in request.form:
        alienid = 12
    elif '13' in request.form:
        alienid = 13
    elif '14' in request.form:
        alienid = 14
    elif '21' in request.form:
        alienid = 21
    elif '22' in request.form:
        alienid = 22
    elif '23' in request.form:
        alienid = 23
    elif '24' in request.form:
        alienid = 24
    elif '31' in request.form:
        alienid = 31
    elif '32' in request.form:
        alienid = 32
    elif '33' in request.form:
        alienid = 33
    elif '34' in request.form:
        alienid = 34
    elif '40' in request.form:
        return render_template('page_9.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # PlanetID 검색하기
    cursor.execute("SELECT planetid FROM alien WHERE alienid = ?", (alienid,))
    planetid = cursor.fetchall()
    planetid = planetid[0][0]

    # Session에 저장한 Team 정보 복구하기
    team_info = session.get('team_info')
    explorerid1 = team_info[0]
    explorerid1 = int(explorerid1)
    explorerid2 = team_info[1]
    explorerid2 = int(explorerid2)
    pilotid = team_info[2]
    pilotid = int(pilotid)
    
    """
    Alien을 포획하기 위해 따질 조건 3가지
    조건 1: 이미 포획한 alien을 다시 포획할 수 없음. 즉, zoo에 있는 alien과 id과 겹치면 안됨
    조건 2: 만약 동물이 ability가 있다면, 같은 ability가 있는 explorer가 한 명이라도 있어야 함
    조건 3: boss 몬스터들은 level 2 조종사가 필요함
    """
    # 조건 1
    cursor.execute("SELECT alienid FROM zoo WHERE alienid = ?", (alienid,))
    alienid_zoo = cursor.fetchall()

    if len(alienid_zoo) == 0:
        cond1 = True
    else:
        cond1 = False

    # 조건 2
    cursor.execute("SELECT ability FROM alien WHERE alienid = ?", (alienid,))
    alien_ability = cursor.fetchall()
    alien_ability = alien_ability[0][0]

    cursor.execute("SELECT major FROM explorer WHERE explorerid = ?", (explorerid1,))
    explorer1_major = cursor.fetchall()
    explorer1_major = explorer1_major[0][0]

    cursor.execute("SELECT major FROM explorer WHERE explorerid = ?", (explorerid2,))
    explorer2_major = cursor.fetchall()
    explorer2_major = explorer2_major[0][0]

    cond2 = True
    if alien_ability == "해일":
        if explorer1_major != "해일" and explorer2_major != "해일": # Explorer 중 해일을 전공한 사람이 있는지 확인하는 코드
           cond2 = False 
    elif alien_ability == "화산":
        if explorer1_major != "화산" and explorer2_major != "화산": # Explorer 중 화산을 전공한 사람이 있는지 확인하는 코드
               cond2 = False 
    elif alien_ability == "지진":
        if explorer1_major != "지진" and explorer2_major != "지진": # Explorer 중 지진을 전공한 사람이 있는지 확인하는 코드
               cond2 = False 
    
    # 조건 3
    cond3 = True
    if alienid == 14 or alienid == 24 or alienid == 34 or alienid == 40: # 만약 Boss 행성 Alien이라면
        cursor.execute("SELECT level FROM pilot WHERE pilotid = ?", (pilotid,))
        pilot_level = cursor.fetchall()
        pilot_level = pilot_level[0][0]
        if pilot_level == 1: # Pilot의 level이 1일 경우 갈 수 없음
            cond3 = False
   
    if cond1 == True and cond2 == True and cond3 == True: # 만약 조건 3개를 모두 만족한다면, 포획에 성공
        cursor.execute("INSERT INTO history (planetid, explorerid1, explorerid2, pilotid, alienid, success) VALUES (?, ?, ?, ?, ?, ?)", 
                        (planetid, explorerid1, explorerid2, pilotid, alienid, 1)) # History 테이블 업데이트
        
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'history'")
        expedition_number = cursor.fetchall()
        expedition_number = int(expedition_number[0][0])
        
        cursor.execute("INSERT INTO zoo (alienid, expeditionnumber) VALUES (?, ?)", (alienid, expedition_number)) # Zoo 테이블까지 업데이트
    else: # 3개 조건을 모두 만족하지 못한 경우
        cursor.execute("INSERT INTO history (planetid, explorerid1, explorerid2, pilotid, alienid, success) VALUES (?, ?, ?, ?, ?, ?)", 
                           (planetid, explorerid1, explorerid2, pilotid, alienid, 0)) # History 테이블 업데이트

    cursor.close()
    conn.commit()
    conn.close()

    return redirect(url_for('page_2'))

if __name__ == '__main__':
    app.run(debug=True)