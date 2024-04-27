from aiogram import  F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json
import app.keyboards as kb



class Reg(StatesGroup):
    distr_chat = State()
    distr_shelter = State()
    
    color = State()
    breed = State()
    
    name = State()
    number = State()


router = Router()


# команда "/start"
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}.  Я - бот PetFinder.\nМоя цель - помогать людям искать потерянных питомцев.\nОсновной инструмент для поиска - *тематические чаты.*', parse_mode="Markdown")
    ans = 'Сейчас доступны следующие опции:\n\n'
    with open('data/options.txt', encoding='utf8') as file:
        for i, option in enumerate(file.readlines(), start=1):
            ans += f'{i}) {option}\n'
    await message.answer(ans, reply_markup= kb.main_reply)


# команда "меню"
@router.message(F.text == 'меню')
async def menu(message: Message, state: FSMContext):
    ans = 'Сейчас доступны следующие опции:\n\n'
    with open('data/options.txt', encoding='utf8') as file:
        for i, option in enumerate(file.readlines(), start=1):
            ans += f'{i}) {option}\n'
    await message.answer(ans, reply_markup= kb.main_reply)
    
    await state.clear()
    
    
# команда "/help"
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Если что-то не работает, попробуйте перезапустить бота.')


# поиск по приютам районов
@router.message(F.text == 'Поиск по району (приюты)')
async def shelter_search(message: Message, state: FSMContext):
    await state.set_state(Reg.distr_shelter)
    await message.answer('Введите название района или округ')
    
@router.message(Reg.distr_shelter)
async def reg_shelter(message: Message, state: FSMContext):
    
    with open('data/shelters.json', encoding='utf8') as shelters:
        
        shelters_data = json.load(shelters)
        if message.text.strip().isupper():
            target = message.text.strip()
        else:
            target = message.text.strip().capitalize()
        
        await message.answer(f'Ищем: {target}...')
        
                
        # поиск по списку приютов
        shelters_ans = []
        for item in shelters_data:
            if target in item['Округ'] or target in item['Район']:
                shelters_ans.append(item)
            
                
                
        if len(shelters_ans) > 0:
            await message.answer('Вот что мне удалось найти:')
            
            for item in shelters_ans:
                res = ''
                for k, v in item.items():
                    res += f'{k} - {v}\n'
                    
                await message.answer(res)
                
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)
            
        else:
            await message.answer('Ничего не нашлось :( \nПроверьте написание и попробуйте снова')
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)





# Поиск по районным чатам
@router.message(F.text == 'Поиск по району (чаты)')
async def distr_search(message: Message, state: FSMContext):
    await state.set_state(Reg.distr_chat)
    await message.answer('Введите название района или округ')
    
@router.message(Reg.distr_chat)
async def reg_distr(message: Message, state: FSMContext):
    
    with open('data/district_chats.json', encoding='utf8') as dst:
        
        dst_data = json.load(dst)
        if message.text.strip().isupper():
            target = message.text.strip()
        else:
            target = message.text.strip().capitalize()
        
        await message.answer(f'Ищем: {target}...')
        
        # поиск по списку районных чатов
        dst_ans = []
        for k, v in dst_data.items():
            if target in k:
                dst_ans.append((k, v))
         
        if len(dst_ans) > 0:
            await message.answer('Вот что мне удалось найти:')
            
            for i in dst_ans:
                await message.answer(f'{i[0]}\n{i[1]}')
                
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)
            
        else:
            await message.answer('Ничего не нашлось :( \nПроверьте написание и попробуйте снова')
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)
            
                                 
        
    



@router.message(F.text == 'Поиск по цвету')
async def color_search(message: Message, state: FSMContext):
    with open('data/colors.json', encoding='utf8') as colors_file:
        colors_data = json.load(colors_file)
        ans='Сейчас поддерживаются следующие варианты:\n'
        for i in colors_data.keys():
            ans += ' * ' + i + '\n'
        await message.answer(ans)
    
    await state.set_state(Reg.color)
    await message.answer('Введите цвет питомца')
    
@router.message(Reg.color)
async def reg_color(message: Message, state: FSMContext):
    
    with open('data/colors.json', encoding='utf8') as colors_file:
        
        colors_data = json.load(colors_file)
        
        if message.text.strip().isupper():
            target = message.text.strip()
        else:
            target = message.text.strip().capitalize()
        
        await message.answer(f'Ищем: {target}...')
        
        
        colors_ans = []
        for k, v in colors_data.items():
            if target in k:
                colors_ans.append((k, v))
         
        if len(colors_ans) > 0:
            await message.answer('Вот что мне удалось найти:')
            
            for i in colors_ans:
                await message.answer(f'{i[0]}\n{i[1]}')
                
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)
            
        else:
            await message.answer('Ничего не нашлось :( \nПроверьте написание и попробуйте снова')
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)



@router.message(F.text == 'Поиск по породе')
async def breed_search(message: Message, state: FSMContext):
    with open('data/breeds.json', encoding='utf8') as breeds_file:
        breeds_data = json.load(breeds_file)
        ans='Сейчас поддерживаются следующие варианты:\n'
        for i in breeds_data.keys():
            ans += ' * ' + i + '\n'
        await message.answer(ans)
    
    await state.set_state(Reg.breed)
    await message.answer('Введите название породы')
    
@router.message(Reg.breed)
async def reg_breed(message: Message, state: FSMContext):
    with open('data/breeds.json', encoding='utf8') as breeds_file:
        
        breeds_data = json.load(breeds_file)
        
        if message.text.strip().isupper():
            target = message.text.strip()
        else:
            target = message.text.strip().capitalize()
        
        await message.answer(f'Ищем: {target}...')
        
        
        breeds_ans = []
        for k, v in breeds_data.items():
            if target in k:
                breeds_ans.append((k, v))
         
        if len(breeds_ans) > 0:
            await message.answer('Вот что мне удалось найти:')
            
            for i in breeds_ans:
                await message.answer(f'{i[0]}\n{i[1]}')
                
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)
            
        else:
            await message.answer('Ничего не нашлось :( \nПроверьте написание и попробуйте снова')
            await message.answer('Чтобы вернуться назад, нажмите конпку "меню" ', reply_markup=kb.return_reply)

    


@router.message(F.text == 'Полезные ссылки')
async def usf_links(message: Message, state: FSMContext):
    await message.answer('Вот полезные ссылки, которые могут вам помочь:')
    with open('data/useful_links.json', encoding='utf8') as useful_links_file:
        data = json.load(useful_links_file)
        for k, v in data.items():
            await message.answer(f'{k} {v}')
            
    
    
    
      
@router.callback_query(F.data == 'dist_search')
async def dist_search(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    Message.answer(text='бимба')
    
@router.callback_query(F.data == 'color_search')
async def color_search(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    
@router.callback_query(F.data == 'breed_search')
async def breed_search(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    
@router.callback_query(F.data == 'useful links')
async def useful_links(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    
    

@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите свое имя')
    
@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')
    
@router.message(Reg.number)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо, регистрация завершена\nИмя: {data["name"]}\nНомер: {data["number"]}')
    await state.clear()