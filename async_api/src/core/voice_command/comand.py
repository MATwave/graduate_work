from pydantic import BaseConfig, BaseModel

class PhraseModel(BaseModel):
    trigger_phrase: tuple
    error_response: str


class TextCommand(BaseConfig):
    welcome: str = 'Добро пожаловать в навык "Практикум". Чем я могу Вам помочь?'
    error: str = 'Извините я не знаю как Вам помочь. Попробуйте еще раз!'
    
    film: PhraseModel = PhraseModel(trigger_phrase=('посоветуй фильм', ),
                                    error_response='Я не смогла найти фильм для рекомендации')
    
    context_film_to_genre: PhraseModel = PhraseModel(trigger_phrase=('жанр у этого фильма', 'жанр у фильма',),
                                                     error_response='Я не смогла определить жанр фильма!')
    
    context_film_to_decription: PhraseModel = PhraseModel(trigger_phrase=('о чем этот фильм', 'о чем фильм', ),
                                                          error_response='Я не смогла найти описание для этого фильма')
    
    context_film_to_actors: PhraseModel = PhraseModel(trigger_phrase=('снялся', 'кто снимался в фильме', ),
                                                      error_response='Я не знаю кто снимался в этом фильме!')
    
    context_genre: PhraseModel = PhraseModel(trigger_phrase=('фильм в таком же жанре', ),
                                             error_response='Я не нашла фильмы в таком же жанре!')
    
    end: tuple = ('спасибо', )
    
    bye: str = 'Рада помочь!'

text_commands = TextCommand()