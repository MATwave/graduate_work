from pydantic import BaseConfig



class TextCommand(BaseConfig):
    welcome: str = 'Добро пожаловать в навык "Практикум". Чем я могу Вам помочь?'
    error: str = 'Извините я не знаю как Вам помочь. Попробуйте еще раз!'
    
    film: tuple = ('найди фильм', 'покажи фильм', 'что за фильм', 'покажи мне фильм')
    context_film_to_genre: tuple = ('жанр у этого фильма', )
    context_film_to_decription: tuple = ('о чем этот фильм', 'о чем фильм', )
    context_film_to_actors: tuple = ('снялся', 'кто снимался в фильме', )

    author: tuple = ('автор фильма', )
    
    end: tuple = ('спасибо', )

text_commands = TextCommand()