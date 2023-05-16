from pydantic import BaseConfig



class TextCommand(BaseConfig):
    welcome: str = 'Добро пожаловать в навык "Практикум". Чем я могу Вам помочь?'
    film: tuple = ('покажи фильм', 'что за фильм')
    author: tuple = ('автор фильма')
    error: str = 'Извените я не знаю как Вам помочь. Попробуйте еще раз!'
    

text_commands = TextCommand()