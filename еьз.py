from requests import get, post

print(get("http://localhost:5000/api/cat/7").json())  # Получить кота через API, хз зачем
print(get("http://localhost:5000/api/cat_list/1").json())  # 1 - это номер страницы, для которой нужны коты
print(post("http://localhost:5000/api/cat_relevant/4", json={"species": "Программист"}).json())
# json может содержать:
# species - порода
# gender - пол
# age - возраст (цифра в текстовом формате [0; 7])
# text - текст, введный в поисковую строку
