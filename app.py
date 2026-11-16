import os
import math
import random
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, 
    url_for, session, flash, jsonify, send_file
)
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# ReportLab 库用于 PDF 导出引擎
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String, Line, PolyLine, Circle
import io

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "trainflow_super_secret_key_2026")

# =====================================================================
# 1. 数据库连接配置 (Database Configuration)
# =====================================================================
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',          # 请根据您的 MySQL 用户名修改
    'password': '',          # 请根据您的 MySQL 密码修改
    'database': 'fitness_db',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    'autocommit': True,
    'connect_timeout': 5,
    'read_timeout': 5,
    'write_timeout': 5
}

FOOD_IMAGE_FILENAMES = {
    '鸡胸肉': 'Chicken Breast.jpg',
    '糙米（熟）': 'Brown Rice.jpg',
    '三文鱼': 'Salmon.jpg',
    '燕麦片': 'Oatmeal.webp',
    '西兰花': 'Broccoli.jpg',
    '鸡蛋': 'Egg.webp',
    '低脂牛奶': 'low-fat-milk.webp',
    '藜麦（熟）': 'quinoa.jpg',
    '希腊酸奶': 'Greek yogurt.jpg',
    '香蕉': 'Banana.jpg',
    '苹果': 'Apple.jpg',
    '地瓜（熟）': 'Cooked sweet potato.jpg',
    '全麦面包': 'Whole wheat bread.jpg',
    '嫩豆腐': 'Soft tofu.jpg',
    '金枪鱼（水浸）': 'Tuna canned in water.jpg',
    '瘦牛肉（熟）': 'Cooked lean beef.jpg',
    '菠菜': 'Spinach.jpg',
    '鹰嘴豆（熟）': 'Cooked chickpeas.webp',
    '牛油果': 'Avocado.webp',
    '低脂茅屋奶酪': 'Low-fat cottage cheese.jpg',
}

FOOD_MEAL_TYPES = {
    '鸡胸肉': {'lunch', 'dinner'},
    '糙米（熟）': {'lunch', 'dinner'},
    '三文鱼': {'lunch', 'dinner'},
    '燕麦片': {'breakfast'},
    '西兰花': {'lunch', 'dinner'},
    '鸡蛋': {'breakfast'},
    '低脂牛奶': {'breakfast'},
    '藜麦（熟）': {'lunch', 'dinner'},
    '希腊酸奶': {'breakfast'},
    '香蕉': {'breakfast'},
    '苹果': {'breakfast'},
    '地瓜（熟）': {'breakfast', 'lunch', 'dinner'},
    '全麦面包': {'breakfast'},
    '嫩豆腐': {'lunch', 'dinner'},
    '金枪鱼（水浸）': {'lunch', 'dinner'},
    '瘦牛肉（熟）': {'lunch', 'dinner'},
    '菠菜': {'lunch', 'dinner'},
    '鹰嘴豆（熟）': {'lunch', 'dinner'},
    '牛油果': {'breakfast', 'lunch', 'dinner'},
    '低脂茅屋奶酪': {'breakfast'},
}

FOOD_COMBINATION_GROUPS = {
    '鸡胸肉': 'main_protein',
    '三文鱼': 'main_protein',
    '瘦牛肉（熟）': 'main_protein',
    '金枪鱼（水浸）': 'main_protein',
    '希腊酸奶': 'dairy',
    '低脂茅屋奶酪': 'dairy',
    '燕麦片': 'staple_carbohydrate',
    '糙米（熟）': 'staple_carbohydrate',
    '藜麦（熟）': 'staple_carbohydrate',
    '地瓜（熟）': 'staple_carbohydrate',
    '全麦面包': 'staple_carbohydrate',
}

FOOD_NUTRITION_ROLES = {
    '燕麦片': {'staple', 'fiber'},
    '糙米（熟）': {'staple', 'fiber'},
    '藜麦（熟）': {'staple', 'protein', 'fiber'},
    '地瓜（熟）': {'staple', 'fiber'},
    '全麦面包': {'staple', 'fiber'},
    '鸡胸肉': {'protein'},
    '三文鱼': {'protein'},
    '鸡蛋': {'protein'},
    '低脂牛奶': {'protein'},
    '希腊酸奶': {'protein'},
    '嫩豆腐': {'protein'},
    '金枪鱼（水浸）': {'protein'},
    '瘦牛肉（熟）': {'protein'},
    '低脂茅屋奶酪': {'protein'},
    '西兰花': {'fiber'},
    '菠菜': {'fiber'},
    '鹰嘴豆（熟）': {'protein', 'fiber'},
    '苹果': {'fiber'},
    '香蕉': {'fiber'},
    '牛油果': {'fiber'},
}

EXERCISE_GIF_FILENAMES = {
    '杠铃卧推': '杠铃卧推.gif',
    '哑铃飞鸟': '哑铃飞鸟.gif',
    '引体向上': '引体向上.gif',
    '杠铃划船': '杠铃划船.gif',
    '杠铃深蹲': '杠铃深蹲.gif',
    '保加利亚分腿蹲': '保加利亚深蹲.gif',
    '哑铃肩上推举': '哑铃肩上推举.gif',
    '侧平举': '侧平举.gif',
    '杠铃弯举': '杠铃弯举.gif',
    '绳索下压': '绳索下压.gif',
    '平板支撑': '平板支撑.gif',
    '卷腹': '卷腹.gif',
    '上斜哑铃推举': '上斜哑铃推举.gif',
    '俯卧撑': '俯卧撑.gif',
    '单臂哑铃划船': '单臂哑铃划船.gif',
    '高位下拉': '高位下拉.gif',
    '罗马尼亚硬拉': '罗马尼亚硬拉.gif',
    '臀桥': '臀桥.gif',
    '面拉': '面拉.gif',
    '俯身反向飞鸟': '俯身反向飞鸟.gif',
    '锤式弯举': '锤式弯举.gif',
    '哑铃三头肌伸展': '哑铃三头肌伸展.gif',
    '俄罗斯转体': '俄罗斯转体.gif',
    '死虫式': '死虫式.gif',
}

def get_db():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)

# =====================================================================
def calculate_bmi(height_cm, weight_kg):
    """
    BMI = Weight (kg) / (Height (m))^2
    """
    if not height_cm or height_cm <= 0 or not weight_kg or weight_kg <= 0:
        return 0, "未知"

    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m * height_m), 1)

    if bmi < 18.5:
        category = "偏瘦"
    elif 18.5 <= bmi <= 23.9:
        category = "正常"
    elif 24.0 <= bmi <= 27.9:
        category = "超重"
    else:
        category = "肥胖"

    return bmi, category

# =====================================================================

def calculate_bmr(gender, age, height_cm, weight_kg):
    """
    Mifflin-St Jeor BMR 公式:
    Male:   10 * weight + 6.25 * height - 5 * age + 5
    Female: 10 * weight + 6.25 * height - 5 * age - 161
    """
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr, 0)

def calculate_tdee(bmr, activity_level):
    """
    TDEE = BMR * Activity Factor
    """
    factors = {
        'sedentary': 1.2,       # 久坐/无运动
        'light': 1.375,         # 轻度运动 (1-3天/周)
        'moderate': 1.55,       # 中度运动 (3-5天/周)
        'active': 1.725,        # 重度运动 (6-7天/周)
        'very_active': 1.9      # 极高强度 (专业训练/体力劳动)
    }
    factor = factors.get(activity_level, 1.55)
    return round(bmr * factor, 0)

def calculate_target_macros(tdee, fitness_goal):
    """
    目标热量与三大营养素配比:
    - 减脂 (cut): TDEE - 500 kcal
    - 维持 (maintain): TDEE
    - 增肌 (bulk): TDEE + 300 kcal
    三大营养素: 蛋白质 (30%), 碳水化合物 (50%), 脂肪 (20%)
    换算: 蛋白质/碳水 4 kcal/g, 脂肪 9 kcal/g
    """
    if fitness_goal == 'cut':
        target_calories = max(tdee - 500, 1200) # 防止摄入过低
        goal_label = '减脂'
    elif fitness_goal == 'bulk':
        target_calories = tdee + 300
        goal_label = '增肌'
    else:
        target_calories = tdee
        goal_label = '维持'

    protein_g = round((target_calories * 0.30) / 4, 1)
    carbs_g = round((target_calories * 0.50) / 4, 1)
    fat_g = round((target_calories * 0.20) / 9, 1)

    return {
        'target_calories': int(target_calories),
        'calorie_adjustment': int(target_calories - tdee),
        'goal_label': goal_label,
        'protein_g': protein_g,
        'carbs_g': carbs_g,
        'fat_g': fat_g
    }

# =====================================================================
# 3. 输入合法性校验与权限拦截器 (Validation & Login Decorator)
# =====================================================================
def validate_profile_input(age, height, weight):
    """验证输入的数值范围限制"""
    if not (10 <= age <= 120):
        return False, "年龄必须在 10 至 120 岁之间"
    if not (50.0 <= height <= 250.0):
        return False, "身高必须在 50cm 至 250cm 之间"
    if not (20.0 <= weight <= 300.0):
        return False, "体重必须在 20kg 至 300kg 之间"
    return True, "OK"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("请先登录系统", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =====================================================================
# 4. 路由与控制层 (Routes & Controllers)
# =====================================================================

@app.route('/')
def index():
    return render_template('index.html')

# ----- 4.1 用户注册 (Register) -----
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_pwd = request.form.get('confirm_password', '')
    age = int(request.form.get('age', 25))
    gender = request.form.get('gender', 'male')
    height = float(request.form.get('height', 170.0))
    weight = float(request.form.get('initial_weight', 70.0))
    activity_level = request.form.get('activity_level', 'moderate')
    fitness_goal = request.form.get('fitness_goal', 'maintain')

    if not username or not password:
        flash("用户名与密码不能为空", "danger")
        return render_template('register.html')

    if password != confirm_pwd:
        flash("两次输入的密码不一致", "danger")
        return render_template('register.html')

    is_valid, msg = validate_profile_input(age, height, weight)
    if not is_valid:
        flash(msg, "danger")
        return render_template('register.html')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash("用户名已被注册，请更换", "danger")
                return render_template('register.html')

            password_hash = generate_password_hash(password)
            sql = """
                INSERT INTO Users (username, password_hash, age, gender, height, initial_weight, activity_level, fitness_goal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (username, password_hash, age, gender, height, weight, activity_level, fitness_goal))

        flash("注册成功！请登录", "success")
        return redirect(url_for('login'))
    finally:
        conn.close()

    return render_template('register.html')

# ----- 4.2 用户登录 (Login) -----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = None
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    flash(f"欢迎回来，{user['username']}！", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("用户名或密码错误", "danger")
        except pymysql.MySQLError:
            flash("数据库暂时无法连接，请确认 XAMPP 的 MySQL 已启动后重试", "danger")
        finally:
            if conn is not None:
                conn.close()

    return render_template('login.html')

# ----- 4.3 注销登录 (Logout) -----
@app.route('/logout')
def logout():
    session.clear()
    flash("已安全退出系统", "info")
    return redirect(url_for('login'))

# ----- 4.4 仪表盘概览 (Dashboard) -----
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            current_weight = user['initial_weight']
            
            bmi, bmi_category = calculate_bmi(user['height'], current_weight)
            bmr = calculate_bmr(user['gender'], user['age'], user['height'], current_weight)
            tdee = calculate_tdee(bmr, user['activity_level'])
            macros = calculate_target_macros(tdee, user['fitness_goal'])

            cursor.execute("""
                SELECT COUNT(*) as count FROM WorkoutLogs 
                WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            """, (user_id,))
            workout_count = cursor.fetchone()['count']

            return render_template(
                'dashboard.html',
                user=user,
                bmi=bmi,
                bmi_category=bmi_category,
                bmr=bmr,
                tdee=tdee,
                macros=macros,
                current_weight=current_weight,
                workout_count=workout_count
            )
    finally:
        conn.close()

# ----- 4.5 智能饮食推荐与检索 (Smart Diet) -----
@app.route('/diet')
@login_required
def diet():
    user_id = session['user_id']
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            bmr = calculate_bmr(user['gender'], user['age'], user['height'], user['initial_weight'])
            tdee = calculate_tdee(bmr, user['activity_level'])
            macros = calculate_target_macros(tdee, user['fitness_goal'])
            target_cal = macros['target_calories']

            breakfast_target = target_cal * 0.25
            lunch_target = target_cal * 0.40
            dinner_target = target_cal * 0.35
            refresh_key = request.args.get('refresh', '')
            active_meal = request.args.get('meal', 'breakfast')
            if active_meal not in ('breakfast', 'lunch', 'dinner'):
                active_meal = 'breakfast'
            recommendation_rng = random.Random(refresh_key or f'{user_id}:{target_cal}')
            next_refresh = secrets.token_urlsafe(8)

            cursor.execute("SELECT * FROM FoodItems")
            foods = cursor.fetchall()
            for food in foods:
                food['image_filename'] = food.get('image_filename') or FOOD_IMAGE_FILENAMES.get(food['name'])

            meal_recommendations = {}
            meal_totals = {}
            selected_food_ids = set()
            meal_targets = {
                'breakfast': breakfast_target,
                'lunch': lunch_target,
                'dinner': dinner_target,
            }
            for meal_type in ('breakfast', 'lunch', 'dinner'):
                dedicated_foods = [
                    food for food in foods
                    if food['meal_type'] == meal_type
                    and food['id'] not in selected_food_ids
                    and meal_type in FOOD_MEAL_TYPES.get(food['name'], {food['meal_type']})
                ]
                flexible_foods = [
                    food for food in foods
                    if food['meal_type'] == 'any'
                    and food['id'] not in selected_food_ids
                    and meal_type in FOOD_MEAL_TYPES.get(food['name'], {meal_type})
                ]
                candidate_foods = dedicated_foods + flexible_foods
                recommendation_rng.shuffle(candidate_foods)
                meal_foods = []
                selected_combination_groups = set()

                def add_food(food):
                    combination_group = FOOD_COMBINATION_GROUPS.get(food['name'])
                    if combination_group and combination_group in selected_combination_groups:
                        return False
                    if food['id'] in {item['id'] for item in meal_foods}:
                        return False
                    meal_foods.append(food)
                    if combination_group:
                        selected_combination_groups.add(combination_group)
                    return True

                # Guarantee one staple, one protein, and one fiber-rich food.
                for role in ('staple', 'protein', 'fiber'):
                    role_candidates = [
                        food for food in candidate_foods
                        if role in FOOD_NUTRITION_ROLES.get(food['name'], set())
                    ]
                    for food in role_candidates:
                        if add_food(food):
                            break

                for food in candidate_foods:
                    if len(meal_foods) == 3:
                        break
                    add_food(food)

                # Food nutrition is stored per 100g. Scale every selected food
                # together so the meal reaches its calorie target without duplicates.
                base_calories = sum(food['calories'] for food in meal_foods)
                scale = meal_targets[meal_type] / base_calories if base_calories else 0
                for food in meal_foods:
                    food['serving_grams'] = round(100 * scale, 1)
                    food['serving_calories'] = round(food['calories'] * scale, 1)
                    food['serving_protein'] = round(food['protein'] * scale, 1)
                    food['serving_carbs'] = round(food['carbs'] * scale, 1)
                    food['serving_fat'] = round(food['fat'] * scale, 1)

                meal_recommendations[meal_type] = meal_foods
                meal_totals[meal_type] = {
                    'calories': round(sum(food['serving_calories'] for food in meal_foods)),
                    'protein': round(sum(food['serving_protein'] for food in meal_foods), 1),
                    'carbs': round(sum(food['serving_carbs'] for food in meal_foods), 1),
                    'fat': round(sum(food['serving_fat'] for food in meal_foods), 1),
                }
                selected_food_ids.update(food['id'] for food in meal_foods)

            return render_template(
                'diet.html',
                user=user,
                macros=macros,
                breakfast_target=breakfast_target,
                lunch_target=lunch_target,
                dinner_target=dinner_target,
                foods=foods,
                meal_recommendations=meal_recommendations,
                meal_totals=meal_totals,
                next_refresh=next_refresh,
                active_meal=active_meal
            )
    finally:
        conn.close()

# ----- 4.6 动作库筛选 (Exercise Library) -----
@app.route('/exercises')
@login_required
def exercises():
    muscle = request.args.get('muscle', 'all')
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            if muscle != 'all' and muscle in ['胸部', '背部', '腿部', '肩部', '手臂', '核心']:
                cursor.execute("SELECT * FROM Exercises WHERE muscle_group = %s", (muscle,))
            else:
                cursor.execute("SELECT * FROM Exercises")
            exercise_list = cursor.fetchall()

            return render_template(
                'exercises.html',
                exercises=exercise_list,
                selected_muscle=muscle,
                exercise_gif_filenames=EXERCISE_GIF_FILENAMES
            )
    finally:
        conn.close()

# ----- 4.7 每日打卡 (Log / Check-in) -----
# 路由路径设为 /log，与函数名 log 及 log.html 完美统一
@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    user_id = session['user_id']
    conn = get_db()
    try:
        if request.method == 'POST':
            log_type = request.form.get('log_type') # 'health' 或 'workout'
            today = datetime.now().date()
            log_date = request.form.get('log_date', today.strftime('%Y-%m-%d'))
            try:
                selected_date = datetime.strptime(log_date, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                flash("请选择有效的打卡日期。", "error")
                return redirect(url_for('log'))

            if selected_date > today:
                flash("打卡日期不能晚于今天。", "error")
                return redirect(url_for('log', date=log_date))

            with conn.cursor() as cursor:
                if log_type == 'health':
                    weight = float(request.form.get('weight'))
                    water = int(request.form.get('water_intake', 0))
                    notes = request.form.get('notes', '')

                    cursor.execute("SELECT height FROM Users WHERE id = %s", (user_id,))
                    user = cursor.fetchone()
                    bmi, _ = calculate_bmi(user['height'], weight)

                    sql = """
                        INSERT INTO HealthLogs (user_id, log_date, weight, bmi, water_intake, notes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE weight=%s, bmi=%s, water_intake=%s, notes=%s
                    """
                    cursor.execute(sql, (user_id, log_date, weight, bmi, water, notes, weight, bmi, water, notes))
                    flash("健康打卡提交成功！", "success")

                elif log_type == 'workout':
                    exercise_name = request.form.get('exercise_name')
                    muscle_group = request.form.get('muscle_group')
                    sets = int(request.form.get('sets'))
                    reps = int(request.form.get('reps'))
                    weight_used = float(request.form.get('weight_used', 0))

                    sql = """
                        INSERT INTO WorkoutLogs (user_id, log_date, exercise_name, muscle_group, sets, reps, weight_used)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (user_id, log_date, exercise_name, muscle_group, sets, reps, weight_used))
                    flash("训练日志记录成功！", "success")

            if log_type == 'health':
                return redirect(url_for('log', date=log_date, clear_health=1))
            return redirect(url_for('log', date=log_date))

        # GET: 加载历史打卡与动作下拉选项
        today = datetime.now().date()
        selected_date = request.args.get('date', today.strftime('%Y-%m-%d'))
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            if selected_date_obj > today:
                selected_date = today.strftime('%Y-%m-%d')
        except (TypeError, ValueError):
            selected_date = today.strftime('%Y-%m-%d')
        clear_health = request.args.get('clear_health') == '1' or 'date' not in request.args

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM HealthLogs WHERE user_id = %s AND log_date = %s ORDER BY id DESC",
                (user_id, selected_date)
            )
            recent_health = cursor.fetchall()

            cursor.execute(
                "SELECT * FROM WorkoutLogs WHERE user_id = %s AND log_date = %s ORDER BY id DESC",
                (user_id, selected_date)
            )
            recent_workouts = cursor.fetchall()

            history_date = request.args.get('history_date', '').strip()
            history_muscle = request.args.get('history_muscle', '').strip()
            history_sql = "SELECT * FROM WorkoutLogs WHERE user_id = %s"
            history_params = [user_id]
            if history_date:
                try:
                    datetime.strptime(history_date, '%Y-%m-%d')
                    history_sql += " AND log_date = %s"
                    history_params.append(history_date)
                except ValueError:
                    history_date = ''
            if history_muscle:
                history_sql += " AND muscle_group = %s"
                history_params.append(history_muscle)
            history_sql += " ORDER BY log_date DESC, id DESC LIMIT 10"
            cursor.execute(history_sql, history_params)
            workout_history = cursor.fetchall()

            cursor.execute("SELECT name, muscle_group FROM Exercises")
            exercises_options = cursor.fetchall()

            cursor.execute(
                "SELECT * FROM HealthLogs WHERE user_id = %s ORDER BY log_date DESC LIMIT 2",
                (user_id,)
            )
            health_summary = cursor.fetchall()

            cursor.execute(
                "SELECT * FROM HealthLogs WHERE user_id = %s AND log_date = %s LIMIT 1",
                (user_id, selected_date)
            )
            selected_health = cursor.fetchone()
            if clear_health:
                selected_health = None

            cursor.execute("SELECT log_date FROM HealthLogs WHERE user_id = %s", (user_id,))
            all_health_dates = cursor.fetchall()

        health_dates = {item['log_date'] for item in all_health_dates}
        streak = 0
        check_date = datetime.now().date()
        while check_date in health_dates:
            streak += 1
            check_date -= timedelta(days=1)

        latest_weight = health_summary[0]['weight'] if health_summary else None
        previous_weight = health_summary[1]['weight'] if len(health_summary) > 1 else None
        weight_change = latest_weight - previous_weight if latest_weight is not None and previous_weight is not None else None

        return render_template(
            'log.html', 
            health_logs=recent_health, 
            workout_logs=recent_workouts,
            workout_history=workout_history,
            history_date=history_date,
            history_muscle=history_muscle,
            exercises_options=exercises_options,
            today=today.strftime('%Y-%m-%d'),
            selected_date=selected_date,
            latest_health=selected_health,
            streak=streak,
            weight_change=weight_change
        )
    finally:
        conn.close()

# ----- 4.8 个人档案修改 (Profile) -----
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                age = int(request.form.get('age', 25))
                gender = request.form.get('gender', 'male')
                height = float(request.form.get('height', 175.0))
                weight = float(request.form.get('weight', 70.0))
                activity_level = request.form.get('activity_level', 'moderate')
                fitness_goal = request.form.get('fitness_goal', 'maintain')

                is_valid, msg = validate_profile_input(age, height, weight)
                if not is_valid:
                    flash(msg, "danger")
                else:
                    sql = """
                        UPDATE Users 
                        SET age=%s, gender=%s, height=%s, initial_weight=%s, activity_level=%s, fitness_goal=%s 
                        WHERE id=%s
                    """
                    cursor.execute(sql, (age, gender, height, weight, activity_level, fitness_goal, user_id))

                    flash("个人档案更新成功！", "success")
                    return redirect(url_for('dashboard'))

            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            profile_weight = user['initial_weight']
            return render_template('profile.html', user=user, profile_weight=profile_weight)
    finally:
        conn.close()

# ----- 4.9 数据分析视图 (Analytics) -----
@app.route('/analytics')
@login_required
def analytics():
    user_id = session['user_id']
    conn = get_db()
    try:
        today = datetime.now().date()
        current_month = today.replace(day=1)
        requested_month = request.args.get('month', current_month.strftime('%Y-%m'))
        try:
            selected_month = datetime.strptime(requested_month, '%Y-%m').date().replace(day=1)
        except (TypeError, ValueError):
            selected_month = current_month
        if selected_month > current_month:
            selected_month = current_month

        if selected_month.month == 12:
            next_month = selected_month.replace(year=selected_month.year + 1, month=1)
        else:
            next_month = selected_month.replace(month=selected_month.month + 1)
        previous_month = selected_month - timedelta(days=1)
        month_end = next_month - timedelta(days=1)

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM HealthLogs
                WHERE user_id = %s
                  AND log_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                ORDER BY log_date ASC
            """, (user_id,))
            health_logs = cursor.fetchall()
            
            cursor.execute("SELECT * FROM WorkoutLogs WHERE user_id = %s ORDER BY log_date ASC", (user_id,))
            workout_logs = cursor.fetchall()

            cursor.execute(
                """
                SELECT log_date, weight, bmi, water_intake, notes FROM HealthLogs
                WHERE user_id = %s AND log_date BETWEEN %s AND %s
                ORDER BY log_date ASC
                """,
                (user_id, selected_month, month_end)
            )
            selected_month_health = cursor.fetchall()

            cursor.execute(
                """
                SELECT log_date, exercise_name, muscle_group, sets, reps, weight_used
                FROM WorkoutLogs
                WHERE user_id = %s AND log_date BETWEEN %s AND %s
                ORDER BY log_date ASC, id ASC
                """,
                (user_id, selected_month, month_end)
            )
            selected_month_workouts = cursor.fetchall()

            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

        recent_health = health_logs
        weight_values = [float(item['weight']) for item in recent_health]
        bmi_values = [float(item['bmi']) for item in recent_health]
        health_dates = [item['log_date'].strftime('%Y-%m-%d') for item in selected_month_health]
        checkin_details = {}
        for item in selected_month_health:
            date_text = item['log_date'].strftime('%Y-%m-%d')
            checkin_details[date_text] = {
                'weight': float(item['weight']),
                'bmi': float(item['bmi']),
                'water': item['water_intake'],
                'notes': item['notes'] or '',
                'workouts': []
            }
        for item in selected_month_workouts:
            date_text = item['log_date'].strftime('%Y-%m-%d')
            checkin_details.setdefault(date_text, {'workouts': []})['workouts'].append({
                'name': item['exercise_name'],
                'muscle': item['muscle_group'],
                'sets': item['sets'],
                'reps': item['reps'],
                'weight': float(item['weight_used'])
            })
        workout_dates = {
            item['log_date'] for item in workout_logs
            if selected_month <= item['log_date'] <= month_end
        }

        return render_template(
            'analytics.html',
            user=user,
            health_logs=health_logs,
            workout_logs=workout_logs,
            recent_health=recent_health,
            weight_values=weight_values,
            bmi_values=bmi_values,
            health_dates=health_dates,
            checkin_details=checkin_details,
            selected_month=selected_month.strftime('%Y-%m'),
            selected_month_label=f'{selected_month.year}年{selected_month.month}月',
            previous_month=previous_month.strftime('%Y-%m'),
            next_month=next_month.strftime('%Y-%m'),
            can_next_month=next_month <= current_month,
            month_checkin_count=len(selected_month_health),
            month_workout_days=len(workout_dates)
        )
    finally:
        conn.close()

# ----- 4.10 报告页面 (Report View) -----
@app.route('/report')
@login_required
def report():
    report_date = request.args.get('date', '').strip()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            date_condition = ""
            query_params = [session['user_id']]
            if report_date:
                date_condition = "AND DATE(generated_at) = %s"
                query_params.append(report_date)
            cursor.execute(
                f"""
                SELECT id, days, generated_at
                FROM ReportHistory
                WHERE user_id = %s
                {date_condition}
                ORDER BY generated_at DESC, id DESC
                LIMIT 6
                """,
                query_params
            )
            report_history = cursor.fetchall()
        return render_template('report.html', report_history=report_history, report_date=report_date)
    finally:
        conn.close()

# ----- 4.11 自动化 PDF 报告导出引擎 (Export PDF) -----
@app.route('/export-pdf')
@login_required
def export_pdf():
    user_id = session['user_id']
    days = int(request.args.get('days', 30))
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            cursor.execute("""
                SELECT * FROM HealthLogs 
                WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                ORDER BY log_date ASC
            """, (user_id, days))
            logs = cursor.fetchall()
            
            cursor.execute("""
                SELECT COUNT(*) as total_workouts FROM WorkoutLogs 
                WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            """, (user_id, days))
            workout_stat = cursor.fetchone()
    finally:
        conn.close()

    # 使用 ReportLab 在内存中生成 PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#10171F'),
        spaceAfter=12
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#5B6670')
    )

    # 过滤非 ASCII 字符避免 ReportLab 默认字体解析崩溃
    username_ascii = user['username'].encode('ascii', 'ignore').decode('ascii') or "User"
    
    story.append(Paragraph(f"TRAINFLOW - Fitness Progress Report ({days} Days)", title_style))
    story.append(Paragraph(f"User: {username_ascii} | Generated Date: {datetime.now().strftime('%Y-%m-%d')}", body_style))
    story.append(Spacer(1, 15))

    latest_weight = logs[-1]['weight'] if logs else user['initial_weight']
    bmi, cat = calculate_bmi(user['height'], latest_weight)
    
    # 将中文分类转换为英文避开字体报错
    cat_en_map = {"偏瘦": "Underweight", "正常": "Normal", "超重": "Overweight", "肥胖": "Obese"}
    cat_en = cat_en_map.get(cat, "Normal")

    summary_data = [
        ['Metric', 'Value'],
        ['Initial Weight', f"{user['initial_weight']} kg"],
        ['Current Weight', f"{latest_weight} kg"],
        ['Current BMI', f"{bmi} ({cat_en})"],
        ['Goal', str(user['fitness_goal']).upper()],
        ['Total Workouts Recorded', str(workout_stat['total_workouts'])]
    ]
    
    t = Table(summary_data, colWidths=[200, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16223A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F7F1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DBE1D6')),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    if logs:
        story.append(Paragraph("<b>Weight Change Chart:</b>", body_style))
        story.append(Spacer(1, 8))

        chart = Drawing(460, 175)
        chart_left, chart_right = 42, 450
        chart_bottom, chart_top = 28, 145
        weights = [float(log_item['weight']) for log_item in logs]
        weight_min = min(weights)
        weight_max = max(weights)
        weight_padding = max(0.5, (weight_max - weight_min) * 0.1)
        axis_min = weight_min - weight_padding
        axis_max = weight_max + weight_padding
        axis_range = axis_max - axis_min

        chart.add(Line(chart_left, chart_bottom, chart_left, chart_top, strokeColor=colors.HexColor('#AAB4BE')))
        chart.add(Line(chart_left, chart_bottom, chart_right, chart_bottom, strokeColor=colors.HexColor('#AAB4BE')))
        for grid_value in (axis_min, (axis_min + axis_max) / 2, axis_max):
            grid_y = chart_bottom + ((grid_value - axis_min) / axis_range) * (chart_top - chart_bottom)
            chart.add(Line(chart_left, grid_y, chart_right, grid_y,
                          strokeColor=colors.HexColor('#DBE1D6'), strokeDashArray=[3, 4]))
            chart.add(String(chart_left - 8, grid_y - 3, f"{grid_value:.1f}",
                             fontName='Helvetica', fontSize=8, textAnchor='end',
                             fillColor=colors.HexColor('#5B6670')))

        points = []
        for index, weight in enumerate(weights):
            x = chart_left if len(weights) == 1 else chart_left + index * (chart_right - chart_left) / (len(weights) - 1)
            y = chart_bottom + ((weight - axis_min) / axis_range) * (chart_top - chart_bottom)
            points.append((x, y))

        if len(points) > 1:
            chart.add(PolyLine([coordinate for point in points for coordinate in point],
                               strokeColor=colors.HexColor('#FF5C4D'), strokeWidth=2.5))
        for x, y in points:
            chart.add(Circle(x, y, 3.5, fillColor=colors.HexColor('#FF5C4D'), strokeColor=None))

        chart.add(String(chart_left, 10, str(logs[0]['log_date']),
                         fontName='Helvetica', fontSize=8, fillColor=colors.HexColor('#5B6670')))
        chart.add(String(chart_right, 10, str(logs[-1]['log_date']),
                         fontName='Helvetica', fontSize=8, textAnchor='end',
                         fillColor=colors.HexColor('#5B6670')))
        story.append(chart)
        story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Recent Weight Logs:</b>", body_style))
    story.append(Spacer(1, 8))
    
    log_table_data = [['Date', 'Weight (kg)', 'BMI', 'Water Intake (ml)']]
    for log_item in logs:
        log_table_data.append([
            str(log_item['log_date']),
            str(log_item['weight']),
            str(log_item['bmi']),
            str(log_item['water_intake'])
        ])
    
    if len(log_table_data) == 1:
        log_table_data.append(['No logs', '-', '-', '-'])

    t_logs = Table(log_table_data, colWidths=[110, 110, 110, 120])
    t_logs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D6FF3F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#10171F')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DBE1D6')),
    ]))
    story.append(t_logs)

    doc.build(story)
    buffer.seek(0)

    history_conn = get_db()
    try:
        with history_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ReportHistory (user_id, days) VALUES (%s, %s)",
                (user_id, days)
            )
    finally:
        history_conn.close()

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"TrainFlow_Report_{username_ascii}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )

# =====================================================================
# 5. 启动入口 (Application Runner)
# =====================================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)