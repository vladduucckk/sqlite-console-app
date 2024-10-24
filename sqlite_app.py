import sqlite3
from datetime import datetime


def movie_age(year: int) -> int:
    """Створення користувацької функції для SQLite"""
    return datetime.today().year - year


try:
    conn = sqlite3.connect('cinema_base.db')  # Підключення до БД

    cursor = conn.cursor()  # Створення курсору

    conn.create_function("movie_age", 1, movie_age)  # Добавляємо користувацьку функцію

    # Створюємо структуру БД, Many : Many, також створюємо зовнішні ключі в таблиці movie_cast
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_year INTEGER,
    genre TEXT);

    CREATE TABLE IF NOT EXISTS actors(
    id INTEGER PRIMARY KEY,
    name TEXT,
    birth_year INTEGER);

    CREATE TABLE IF NOT EXISTS movie_cast(
    movie_id INTEGER,
    actor_id INTEGER,
    CONSTRAINT fk_mv_id FOREIGN KEY (movie_id) REFERENCES movies(id),
    CONSTRAINT fk_ac_it FOREIGN KEY (actor_id) REFERENCES actors(id))""")

    # Запускаємо нескінченний цикл, з якого можемо вийти за допомогою (0)
    while True:
        print("""
1. Додати фільм
2. Додати актора
3. Показати всі фільми з акторами
4. Показати унікальні жанри
5. Показати кількість фільмів за жанром
6. Показати середній рік народження акторів у фільмах певного жанру
7. Пошук фільму за назвою
8. Показати фільми (з пагінацією)
9. Показати імена всіх акторів та назви всіх фільмів
10. Додаткове завдання(movie_age())
0. Вихід""")
        action = input("\nВиберіть дію(1-10), або (0) для завершення: ")
        match int(action):
            case 1:
                """Додаємо фільм"""
                name_f = input("Назва(str): ")
                release_f = int(input("Рік виходу(int): "))
                genre_f = input("Жанр(str): ")

                data = (name_f, release_f, genre_f)  # Кортеж для execute

                cursor.execute("""
                INSERT INTO movies(title, release_year, genre)
                VALUES(?,?,?)""", data)  # Виконуємо запит із вставкою, розпаковуємо кортеж

                conn.commit()  # Зберігаєм в БД, потрібно виконувати після INSERT,UPDATE,DELETE

                print("\nСписок існуючих акторів:")

                cursor.execute("SELECT * FROM actors")  # Робимо виборку із всих полів таблиці актори

                available_actor = cursor.fetchall()  # Отримуємо всі записи

                for actor in available_actor:  # Проганяємо через цикл, щоб отримати кожний запис
                    print("id:", actor[0], "\nname:", actor[1], "\nbirth_year:", actor[2])

                while True:

                    actor_id = int(input("Додай актора для фільма(поле id),або заверши дію (0): "))
                    if int(actor_id) == 0:  # Якщо акторів немає, користувач може завершити дію
                        break

                    cursor.execute("""SELECT COUNT(id) FROM movies""")  # Отримуємо кількість id

                    movie_id = cursor.fetchone()[0]  # Отримуємо перший запис
                    # в кортеж піде actor_id якого добавив користувач, та movie_id який створився
                    data_movie = (movie_id, actor_id)  # Кортеж для execute

                    cursor.execute("""
                    INSERT INTO movie_cast(movie_id, actor_id)
                    VALUES(?,?)""", data_movie)

                    conn.commit()

            case 2:
                """Додаємо актора"""
                # Робимо все те саме що і для case 1
                name_a = input("Ім'я актора(str): ")
                birth_a = int(input("Рік народження(int): "))

                data = (name_a, birth_a)

                cursor.execute("""
                INSERT INTO actors(name,birth_year)
                VALUES(?,?)""", data)

                conn.commit()

            case 3:
                """Джойнимо через 3 таблиці"""

                cursor.execute("""
                SELECT movies.title, actors.name
                FROM movies INNER JOIN movie_cast ON movies.id = movie_cast.movie_id
                JOIN actors ON movie_cast.actor_id = actors.id""")

                join_rezult = cursor.fetchall()
                for i in join_rezult:
                    print(f"Фільм: {i[0]}, Актор: {i[1]}")

            case 4:
                """За допомогою Distinct отримуємо унікальні записи"""
                print("Унікальні жанри")
                cursor.execute("""SELECT DISTINCT(genre) FROM movies""")
                distinct_genres = cursor.fetchall()

                for genre in distinct_genres:
                    print(genre[0])
            case 5:
                """За допомогою Group by та агрегації отримуємо кількість фільмів для жанрів """
                print("Кількість фільмів для кожного жанру")

                cursor.execute("""
                SELECT genre ,COUNT(genre)
                FROM movies
                GROUP BY genre""")

                count = cursor.fetchall()  # Отримуємо всі записи
                for i in count:
                    print(f"Жанр: {i[0]}, Кількість: {i[1]}")

            case 6:
                """Спочатку джойнимо,а потім з допомогою Group By та агрегації отримуємо результат"""
                print("Середній рік народження акторів різних жанрів")

                cursor.execute("""
                SELECT movies.genre, AVG(actors.birth_year) 
                FROM movies INNER JOIN movie_cast ON movies.id = movie_cast.movie_id
                JOIN actors ON movie_cast.actor_id = actors.id
                GROUP BY movies.genre""")

                data = cursor.fetchall()
                for i in data:
                    print(f"Жанр: {i[0]}, Середній рік народження: {i[1]}")

            case 7:
                """Використання Like"""
                print("Пошук фільму за назвою")
                name_film = input("Введіть назву фільму або фрагмент: ")
                pattern = f"{name_film}%"

                cursor.execute("""
                SELECT * FROM movies
                WHERE title LIKE ? """, (pattern,))

                print("Знайдені фільми:")

                films = cursor.fetchall()

                for film in films:
                    print(f"Назва: {film[1]}, Рік: {film[2]}, Жанр: {film[3]}")

            case 8:
                """Пагінація, яка дає користувачу можливість вибирати кількість фільмів для page"""
                print("Показ фільмів з пагінацією")
                # Отримуємо кількість фільмів, щоб потім зробити математичні підрахунки
                cursor.execute("""SELECT COUNT(title) FROM movies""")

                count_film = cursor.fetchone()[0]

                print("Кількість фільмів:", count_film)

                question_limit = int(input("Скільки ви хочете бачити фільмів на сторінці: "))
                # Кількість повних сторінок
                calculation = count_film // question_limit
                # Сторінка, яка може бути неповною, або взагалі її може не бути
                calculation_remainder = count_film % question_limit

                print(f"Вам доступні {calculation} сторінки по {question_limit} фільмів")

                if calculation_remainder > 0:
                    print(f"Також {calculation + 1} сторінка на {calculation_remainder} фільмів")

                page = int(input("Яку сторінку бажаєте відкрити: "))
                # Знаходимо OFFSET, так як LIMIT та page вже вказав користувач
                offset = (page - 1) * question_limit

                # Параметри для execute
                pagin = (question_limit, offset)

                cursor.execute("""
                SELECT id,title FROM movies
                LIMIT ?
                OFFSET ?""", pagin)

                data = cursor.fetchall()

                for i in data:
                    print(f"{i[0]}.{i[1]}")

            case 9:
                """Приклад роботи Union"""
                print("Імена всіх акторів та назви всіх фільмів")

                cursor.execute("""
                SELECT name FROM actors
                UNION 
                SELECT title FROM movies""")

                actors_movies = cursor.fetchall()

                for i in actors_movies:
                    print(i[0])

            case 10:
                """Робота користувацької функції"""
                print("Фільми та їх вік:")

                cursor.execute("""SELECT title,movie_age(release_year) FROM movies""")

                films_year = cursor.fetchall()

                for i in films_year:
                    print(f"Назва: {i[0]}, Вік: {i[1]}")

            case 0:
                """Заверщення программи"""
                break

except sqlite3.Error as error:
    print("Помилка при роботі з БД", error)

except ValueError as error:
    print(error)

# finally спрацює в любому випадку й закриє з'єднання з БД
finally:
    if conn:
        conn.close()
        print("З'єднання з БД закрито")
