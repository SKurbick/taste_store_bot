LEXICON_RU: dict[str, str] = {
    '/start': "start message",
    "/start_manager": "ты менеджер - тут должно быть ответное сообщение для тебя",
    '/start_buyer': "Чтобы сформировать коммерческое предложение отправьте команду /comm_offer",
    'comm_offer_button': "Коммерческое предложение",
    'cancel_comm_offer': "Вы отменили формирование комм. проедложения",
    'comm_offer': "Старт формирования комм. предложения.\nПришлите наименование продукта:",
    '/help': "",
    '/registration': "registration",
    '/what_status': "status",
    '/buyer': "buyer",
    '/manager': "manager",
    '/admin': "admin",
    '/registration_status': "Ваша заявка на регистрацию в обработке, можете напрямую связаться с вашим менеджером что бы ускорить процесс регистрации",
    '/registration_action': "Пользователь {} отправил запрос на регистрацию.\nНомер для связи: {}\nПодтвердите дальнейшие действия:",
    'reg_username': "Приятно познакомиться, {}\nТеперь пришлите ваш номер телефона, для дальнейших коммуникаций: формат - 89997776655",
    'reg_phone_number': "Отлично! Осталось только подтвердить регистрацию и мы оповестим об этом администратора бота:",
    'role_give': "Определите роль для нового пользователя",
    '/show_all_users': "Вас интересует список зарегистрированных менеджеров или закупщиков?",
    '/delete_user': "Чтобы удалить пользователя нужно знать его id. Если не знаете id - отправьте команду /show_all_users, чтобы узнать какой id у пользователя. Если вы знаете id пользователя нажмите на кнопку под сообщением.",
    'delete_user_finish': "Найден пользователь {}. Вы действительно хотите удалить этого пользователя?\nЕму больше не будут доступны права для использования возможностей бота.",
    'result_action_message_buyer':"Товар: {}\nСтрана: {}\nЦена б/н: {} за {}\nКомментарий: {}",

}
data_translate = {
    'thing': "шт",
    'kg': "кг"
}

help_message = {
    "help_buyer": "Чтобы сформировать коммерческое предложение, отправьте команду /comm_offer."
                  "После окончания её формирования и подтверждение, она будет переслана менеджеру компании. \n"
                  "Чтобы посмотреть  весь список ваших ком. пред-ий за день, отправьте команду /show_my_offers.\n"
                  "/commands - выведет весь список доступных команд.",

    "help_manager": "В течении дня вам будет приходить сформированное коммерческое предложение по товару.\n"
                    "/show_offers - покажет вам все дневные ком. пред-я, если вы вдруг могли их пропустить",

    "help_admin": "Регистрирация пользователей проходит только после вашего согласия. Пользователь должен заполнить форму,"
                  " следом к вам придёт подтверждение и выбор роли (менеджер\закупщик) по данному пользователю."
                  "Сформированное коммерческое предложение закупщика направляется сразу менеджеру(клиенту). Коммерческое предложение"
                  "проходит определенный 'фильтр' по цене, который вами будет установлен.\n"
                  "/show_all_users - отобразит всех пользователей зарегестрированных через бота.\n"
                  "/delete_user - поможет вам с удалением пользователя\n\n"
                  "P.S.Для более подробной информации или помощи с расширением функционала обращайтесь к @SKurbick.\n"
                  "Торговли!",

}

command_role = {
    "command_buyer": "/comm_offer - сформировать коммерческое предложение.\n/show_my_offers - посмотреть все ком. пред. за день.\n/help - помощь с навигацией бота.",

    "command_manager": "/show_offers - просмотр ком. пред-ий за день\n/help - помощь с навигацией бота.",
    "command_admin": "/show_all_users - показать зарег. пользователей.\n/delete_user - удалить пользователя.\n/help - помощь с навгицией бота."

}
