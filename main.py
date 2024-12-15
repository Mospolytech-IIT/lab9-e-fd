from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Создаем базовый класс для модели
Base = declarative_base()


# Определяем модель таблицы Users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Связь с таблицей Posts
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


# Определяем модель таблицы Posts
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Связь с таблицей Users
    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, user_id={self.user_id})"


# Создаем подключение к базе данных SQLite
engine = create_engine('sqlite:///database.db', echo=True)

# Создаем все таблицы
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример добавления пользователей и постов
new_user = User(username="johndoe", email="johndoe@example.com", password="securepassword123")
session.add(new_user)
session.commit()

new_post = Post(title="My first post", content="This is the content of the post", user_id=new_user.id)
session.add(new_post)
session.commit()

print("Tables created and data inserted successfully!")

# Добавление нескольких записей в таблицу Users
users = [
    User(username="alice", email="alice@example.com", password="password1"),
    User(username="bob", email="bob@example.com", password="password2"),
    User(username="charlie", email="charlie@example.com", password="password3")
]

session.add_all(users)
session.commit()
print("Users added successfully!")

# Добавление нескольких записей в таблицу Posts
posts = [
    Post(title="Alice's First Post", content="Hello, this is Alice!", user_id=1),
    Post(title="Bob's Introduction", content="Hey, Bob here.", user_id=2),
    Post(title="Charlie's Story", content="Once upon a time...", user_id=3),
    Post(title="Alice's Second Post", content="Another post from Alice!", user_id=1)
]

session.add_all(posts)
session.commit()
print("Posts added successfully!")

users = session.query(User).all()
for user in users:
    print(user)

posts = session.query(Post).join(User).all()
for post in posts:
    print(f"Post: {post.title}, Author: {post.author.username}")

username = "alice"
user_posts = session.query(Post).join(User).filter(User.username == username).all()
for post in user_posts:
    print(f"Post by {username}: {post.title}")

user_to_update = session.query(User).filter(User.username == "bob").first()
if user_to_update:
    user_to_update.email = "newbob@example.com"
    session.commit()
    print("User email updated successfully!")

post_to_update = session.query(Post).filter(Post.title == "Charlie's Story").first()
if post_to_update:
    post_to_update.content = "Updated story content."
    session.commit()
    print("Post content updated successfully!")

post_to_delete = session.query(Post).filter(Post.title == "Alice's Second Post").first()
if post_to_delete:
    session.delete(post_to_delete)
    session.commit()
    print("Post deleted successfully!")

user_to_delete = session.query(User).filter(User.username == "alice").first()
if user_to_delete:
    session.query(Post).filter(Post.user_id == user_to_delete.id).delete()
    session.delete(user_to_delete)
    session.commit()
    print("User and their posts deleted successfully!")

