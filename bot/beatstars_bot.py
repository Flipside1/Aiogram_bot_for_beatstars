from selenium import webdriver
from selenium.webdriver.common.by import By

import logging
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import os
import time
import random

from colorama import Back, Fore

from create_bot import bot, dp
from other.keyboard import *
from other.comments import list_comments

username = None
password = None
code = None
username_inp = None
password_inp = None
code_inp = None


agree = None
find_element = None
sent_code = None

logging.basicConfig(level=logging.INFO)


class Form0(StatesGroup):
    username_inp = State()
    password_inp = State()


class Form1(StatesGroup):
    code_inp = State()


class BeatstarsBot:
    """Класс работы бота"""

    def __init__(self):
        """Переменные для входа в аккаунт"""

        self.data = None
        self.list_comment = None
        self.profile_urls = None
        self.profile_url = None
        self.sleep_1_cycle = None
        self.sleep_day_cycle = None
        self.number = None
        self.browser = None

    def oauth_beatstars(self):
        """Открывает страницу авторизации в битстарс"""

        try:
            print(Fore.LIGHTMAGENTA_EX, "Захожу в браузер, подождите...")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            self.browser = webdriver.Firefox()
            self.browser.get('https://oauth.beatstars.com/')
            time.sleep(random.randrange(5, 15))

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось открыть битстарс, запускаю авторизацию заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars()

    def username_input(self):
        """Вводит логин"""
        try:
            username_input = self.browser.find_element(By.XPATH, '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[1]/bs-text-input/input')
            username_input.click()
            time.sleep(random.randrange(2, 4))
            username_input.clear()
            username_input.send_keys(username)

            print(Fore.LIGHTWHITE_EX, "Бот ввёл имя пользователя!")
            time.sleep(random.randrange(2, 4))

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось ввести имя пользователя, запускаю авторизацию заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.username_input()

    def password_input(self):
        """Вводит пароль"""

        try:
            password_input = self.browser.find_element(By.XPATH, '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[2]/bs-text-input/input')
            password_input.click()
            time.sleep(random.randrange(2, 5))
            password_input.clear()
            password_input.send_keys(password)

            print(Fore.LIGHTWHITE_EX, "Бот ввёл пароль!")
            time.sleep(random.randrange(1, 3))

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось ввести пароль, запускаю авторизацию заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.password_input()

    def login_button(self):
        """Нажимает на кнопку 'Войти' """

        try:
            login_button = self.browser.find_element(By.XPATH,
                                                     '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/bs-square-button/button')
            login_button.click()
            print(Fore.LIGHTWHITE_EX, "Нажал на кнопку войти")
            time.sleep(random.randrange(20, 30))

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось нажать на кнопку "Войти", запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))

    def send_code(self):
        """Отправляет код подтверждения"""

        global sent_code

        try:
            time.sleep(random.randrange(15, 25))
            self.browser.find_element(By.XPATH,
                                      '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[3]')
            sent_code = 'yes'

            try:
                code_1 = self.browser.find_element(By.XPATH,
                                                   '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[3]')
                code_1.click()
                code_1.send_keys(code[0])

                code_2 = self.browser.find_element(By.XPATH,
                                                   '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[4]')
                code_2.click()
                code_2.send_keys(code[1])

                code_3 = self.browser.find_element(By.XPATH,
                                                   '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[5]')
                code_3.click()
                code_3.send_keys(code[2])

                code_4 = self.browser.find_element(By.XPATH,
                                                   '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[6]')
                code_4.click()
                code_4.send_keys(code[3])
                time.sleep(random.randrange(35, 45))
                self.find_elements_for_code()

            except Exception as ex:
                print(Fore.LIGHTRED_EX, 'Не получилось ввести код верификации')
                print(Fore.RED, 'Описание ошибки: ', ex)

        except:
            sent_code = 'not'
            self.agree_to_cookies()

    def find_elements_for_code(self):
        """Находит элемент на сайте, чтобы подтвердить, что код верификации введен верно"""

        global find_element
        try:
            self.browser.find_element(By.XPATH,
                                      '/html/body/mp-root/mp-snackbar-info-messages/div/mp-cookies-snackbar/mp-snackbar-info-message-template/div/button')
            find_element = 1

        except Exception as ex:
            find_element = None
            print(Fore.LIGHTRED_EX, 'Введен неверный код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def agree_to_cookies(self):
        """Нажимает на кнопку 'Согласиться с куки' """

        global agree
        try:
            cookie_consent = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/mp-snackbar-info-messages/div/mp-cookies-snackbar/mp-snackbar-info-message-template/div/button')
            cookie_consent.click()
            agree = 1

        except Exception as ex:
            agree = None
            print(Fore.LIGHTRED_EX, 'Не получилось согласиться с куки, попробуйте еще раз через некоторое время')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def open_feed(self):
        """Открывает фид"""

        try:
            self.browser.get('https://www.beatstars.com/feed')
            print(Fore.LIGHTYELLOW_EX, ' Открыл фид!')
            time.sleep(random.randrange(10, 20))

            self.play_beat()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось открыть фид, пробую заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def play_beat(self):
        """Нажимает на кнопку включения бита"""

        try:
            play_button = self.browser.find_element(By.XPATH,
                                                    '/html/body/mp-root/div/div/ng-component/mp-feed/div/section[2]/div[1]/mp-track-post/mp-feed-card/div/div[2]/div[1]/div[2]/div[1]/bs-button-play-item/button')
            play_button.click()
            print(Fore.LIGHTGREEN_EX, 'Включил бит')
            time.sleep(random.randrange(5, 10))

            self.open_beat()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось нажать на кнопку включения бита, запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def open_beat(self):
        """Открывает описание бита"""

        try:
            opening_beat = self.browser.find_element(By.XPATH,
                                                     '//*[@id="player-container"]/div/div[1]/div[1]/bs-playable-item-info/div[2]/div[1]/a')
            opening_beat.click()

            print(Fore.LIGHTGREEN_EX, 'Открыл описание бита')
            time.sleep(random.randrange(10, 15))

            self.comments()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось открыть описание бита, запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def like(self):
        """Нажимает на кнопку лайка в описании бита"""

        try:
            like_button = self.browser.find_element(By.XPATH,
                                                    '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-like-action-template')
            like_button.click()
            print(Fore.LIGHTYELLOW_EX, 'Поставил лайк')
            time.sleep(random.randrange(3, 7))

            self.cycle_to_liked()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось поставить лайк, пишу комментарий.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.cycle_to_liked()

    def comment(self):
        """Определяет рандомный комментарий"""

        self.list_comment = random.choice(list_comments)

    def comments(self):
        """Печатает и отправляет комментарии"""

        try:
            self.comment()

            # нажимает на поле ввода и пишет рандомный комментарий
            input_comments = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[3]/div[2]/mp-comments-panel-box/mp-open-close-panel-template/div/article/div[2]/mp-create-new-comment-input/mp-musician-autocomplete-wrapper/mp-autocomplete-dropdown-template/div/div[2]/mp-compose-new-message-input/form/div[2]/input')
            time.sleep(random.randrange(5, 10))
            input_comments.send_keys(self.list_comment)
            print(Fore.GREEN, "Ввёл комментарий:", self.list_comment)

            # нажимает на кнопку отправки комментария
            comment_button = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[3]/div[2]/mp-comments-panel-box/mp-open-close-panel-template/div/article/div[2]/mp-create-new-comment-input/mp-musician-autocomplete-wrapper/mp-autocomplete-dropdown-template/div/div[2]/mp-compose-new-message-input/form/bs-square-button')
            comment_button.click()
            print(Fore.LIGHTGREEN_EX, 'Отправил комментарий!')
            time.sleep(random.randrange(5, 15))

            self.open_profile()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось отправить комментарий, открываю профиль')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_profile()

    def open_profile(self):
        """Открывает профиль"""

        try:
            go_to_the_profile = self.browser.find_element(By.XPATH,
                                                          '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[2]/mp-caption-figure-template[2]/a')
            go_to_the_profile.click()
            print(Fore.LIGHTCYAN_EX, 'Открыл профиль, сейчас посмотрим, что тут у нас')
            time.sleep(random.randrange(15, 25))

            self.subscription()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось открыть профиль, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def subscription(self):
        """Подписывается на пользователя"""

        try:
            follow_button = self.browser.find_element(By.XPATH,
                                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-wrapper-member-profile-content/main/bs-container-grid/mp-profile-header/mp-profile-visitor-actions/div/mp-button-follow-text-template/mp-button-item-action-text-template')
            follow_button.click()
            print(Fore.LIGHTBLUE_EX, 'Оформил подписку!')
            time.sleep(random.randrange(5, 15))

            self.back()
            self.open_liked()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Подписаться не получилось, нажимаю кнопку "Назад".')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.back()

    def back(self):
        """Нажимает на кнопку 'Назад' в браузере"""

        try:
            self.browser.back()
            print(Fore.LIGHTGREEN_EX, 'Нажал на кнопку "Назад"')
            time.sleep(random.randrange(10, 15))

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось нажать на кнопку "Назад", запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def close_menu(self):
        """Закрывает меню с лайнкувшими"""

        try:
            self.browser.find_element(By.CSS_SELECTOR, '.close-button').click()
            print(Fore.LIGHTGREEN_EX, 'Закрыл меню с лайкнувшими')
            time.sleep(random.randrange(2, 4))
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось закрыть меню, запускаю алгоритм подписки на лайкнувших.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.cycle_to_liked()

    def open_liked(self):
        """Открывает меню с лайкнувшими"""
        try:
            likes = self.browser.find_element(By.XPATH,
                                              '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-like-action-template/mp-button-item-action-icon-template/span')
            likes.click()
            print(Fore.LIGHTYELLOW_EX, 'Открыл меню с лайкнувшими!')
            time.sleep(random.randrange(7, 15))

            self.parsing()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось открыть меню лайкнувших, запускаю цикл заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def parsing(self):
        """Парсит ссылки на тех, кто лайкнул бит"""

        try:

            # ищет элементы только в окне с теми, кто лайкнул бит
            window_with_liked = self.browser.find_element(By.CLASS_NAME, 'body-container')

            # ищет элементы с тегом "а"
            elements = window_with_liked.find_elements(By.TAG_NAME, 'a')

            # собирает ссылки на элементы только 'href'
            self.profile_urls = [item.get_attribute('href') for item in elements]

            print(Fore.LIGHTCYAN_EX, 'Спарсил ссылки на профили: ', Fore.LIGHTYELLOW_EX, self.profile_urls)

            self.close_menu()
            self.like()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось спарсить пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def cycle_to_liked(self):
        """Запускает цикл подписки на лайкнувших"""

        try:
            for self.profile_url in self.profile_urls[0:random.randrange(3, 8)]:
                self.browser.get(self.profile_url)
                time.sleep(random.randrange(10, 15))

                self.subscription_to_liked()
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось запустить цикл подписки на пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed()

    def subscription_to_liked(self):
        """Подписывается на лайкнувших"""

        try:

            follow_button = self.browser.find_element(By.XPATH,
                                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-wrapper-member-profile-content/main/bs-container-grid/mp-profile-header/mp-profile-visitor-actions/div/mp-button-follow-text-template/mp-button-item-action-text-template')
            follow_button.click()
            print(Fore.LIGHTGREEN_EX, 'Оформил', Fore.LIGHTBLUE_EX, 'подписку', Fore.LIGHTGREEN_EX, 'на:',
                  Fore.LIGHTYELLOW_EX, self.profile_url)

            time.sleep(random.randrange(30, 45))
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось подписаться на "', self.profile_url,
                  '", подписываюсь на следующего пользователя.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(10)

    def close_beatstars(self):
        """Открывает страницу гугл, якобы для закрытия битстарса"""

        self.browser.get('https://google.com/')
        print('Бот закрыл битстарс')

    def stop_bot(self):
        """Полностью закрывает браузер"""

        self.browser.quit()
        print('Бот закрыл браузер')

    def sleep(self):
        """Рандомизирует переменные сна"""

        self.sleep_1_cycle = random.randrange(3500, 5500)
        self.sleep_day_cycle = random.randrange(27000, 40000)

    def repost_beat(self):
        """Делает репост моих битов"""

        try:
            self.browser.get('https://www.beatstars.com/flipsidebeats/tracks')
            time.sleep(random.randrange(30, 40))

            self.browser.find_element(By.XPATH,
                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-search-v3/div/div/section/mp-search-results/mp-list-card-track/div/mp-list-card-template/div/mp-card-figure-track[1]/mp-card-figure-template/figure/div/div[2]/div[2]/mp-button-play-track-on-algolia-v3/bs-vb-button-play-item').click()
            time.sleep(random.randrange(3, 5))

            for i in range(0, random.randrange(1, 4)):
                # открывает описание бита
                self.browser.find_element(By.XPATH,
                                          '//*[@id="player-container"]/div/div[1]/div[1]/bs-playable-item-info/div[2]/div[1]/a').click()
                print(Fore.LIGHTWHITE_EX, 'Открыл описание бита')
                time.sleep(random.randrange(15, 20))

                # нажимает на кнопку репоста (2 раза)
                self.browser.find_element(By.XPATH,
                                          '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-repost-icon-template/mp-button-item-action-icon-template/button').click()
                time.sleep(random.randrange(2, 4))
                print(Fore.LIGHTYELLOW_EX, 'Сделал репост')

                # переключает на следующий бит
                self.browser.find_element(By.XPATH,
                                          '/html/body/mp-root/mp-player-wrapper/bs-player/div/div/div[2]/bs-player-next/button').click()
                print(Fore.LIGHTCYAN_EX, 'Переключился на следующий бит')
                time.sleep(random.randrange(5, 10))
        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Не получилось сделать репост')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(10)

    def start_bot(self):
        """Запускает цикличную работу бота"""

        try:
            work_bot = True

            while work_bot:
                """Бесконечный цикл"""

                self.sleep()

                for main_cycle in range(0, 1):
                    """Выполняется 1 раз в день, засыпает на 8-12 часов"""

                    self.sleep()

                    for self.number in range(0, random.randrange(3, 7)):
                        """Выполняется 3, 7 раз в день, каждый раз засыпает на 1-1,5 часа"""

                        self.sleep()

                        for i in range(0, random.randrange(14, 25)):
                            """Сам цикл, выполняется 4-7 раз за 1 цикл"""

                            self.open_feed()
                            print(Fore.LIGHTYELLOW_EX, 'Цикл номер', i + 1, 'успешно завершён! Продолжаем..')
                            time.sleep(random.randrange(5, 15))

                        self.close_beatstars()
                        print(Fore.LIGHTMAGENTA_EX, 'Циклы завершены. Боту нужно немного отдохнуть...'
                                                    'Он продолжит работу через: ', self.sleep_1_cycle)
                        time.sleep(self.sleep_1_cycle)

                    print(Fore.LIGHTYELLOW_EX, 'Бот провёл', self.number, 'циклов за день!')

                print('Боту тоже нужен сон! Он проснётся через: ', self.sleep_day_cycle)

                time.sleep(self.sleep_day_cycle)

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.browser.get('https://google.com/')

    def start_bot_with_reposts(self):
        """Запускает цикличную работу бота + репост битов"""
        try:
            work_bot = True

            while work_bot:
                """Бесконечный цикл"""

                self.sleep()

                for main_cycle in range(0, 1):
                    """Выполняется 1 раз в день, засыпает на 8-12 часов"""

                    print("Бот начал репостить твои биты!")
                    self.sleep()
                    self.repost_beat()

                    for self.number in range(0, random.randrange(3, 7)):
                        """Выполняется 3, 7 раз в день, каждый раз засыпает на 1-1,5 часа"""

                        self.sleep()

                        for i in range(0, random.randrange(14, 25)):
                            """Сам цикл, выполняется 4-7 раз за 1 цикл"""

                            self.open_feed()
                            print(Fore.LIGHTYELLOW_EX, 'Цикл номер', i + 1, 'успешно завершён! Продолжаем..')
                            time.sleep(random.randrange(5, 15))

                        self.close_beatstars()
                        print(Fore.LIGHTMAGENTA_EX, 'Циклы завершены. Боту нужно немного отдохнуть...'
                                                    'Он продолжит работу через: ', self.sleep_1_cycle)
                        time.sleep(self.sleep_1_cycle)

                    self.repost_beat()
                    print(Fore.LIGHTYELLOW_EX, 'Бот провёл', self.number, 'циклов за день!')

                print('Боту тоже нужен сон! Он проснётся через: ', self.sleep_day_cycle)
                time.sleep(self.sleep_day_cycle)

        except Exception as ex:
            print(Fore.LIGHTRED_EX, 'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.browser.get('https://google.com/')


beat_bot = BeatstarsBot()


# уведомляет об успешном запуске бота
async def on_startup(message):
    print(Back.BLACK, Fore.LIGHTWHITE_EX, "Бот вышел в онлайн!")


# отвечает на команду /start и /help
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет, я бот, помогающий раскрутить твой битстарс аккаунт!", reply_markup=keyboard_start)


# начинаем собирать данные для авторизации от пользователя
@dp.message_handler(commands='start_input_data', state=None)
async def start_input_data():
    await Form0.username_inp.set()


# выход из машинных состояний
@dp.message_handler(state="*", commands='Отменить запись данных')
@dp.message_handler(Text(equals='Отменить запись данных', ignore_case=True), state="*")
async def cancel_input_data(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ввод данных отменён!', reply_markup=keyboard_send_data)


# ловим имя пользователя и записываем его в словарь
@dp.message_handler(state=Form0.username_inp)
async def input_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username_inp'] = message.text
    await Form0.next()
    await message.reply('Теперь введи пароль')


# ловим пароль, записываем его в словарь и записываем полученные данные (имя пользователя и пароль) в переменные
@dp.message_handler(state=Form0.password_inp)
async def input_password(message: types.Message, state: FSMContext):
    global username, password

    async with state.proxy() as data:
        data['password_inp'] = message.text
        username = str(data['username_inp'])
        password = str(data['password_inp'])
        await bot.send_message(message.from_user.id, 'Отлично, данные для авторизации введены!\nТеперь нажми на "Отправить данные на сайт.\n'
                                                     'Если данные введены неверно, то нажмите на кнопку "Ввести данные авторизации" еще раз.',
                               reply_markup=keyboard_send_data)

    await state.finish()


# запрашиваем от пользователя код подтверждения (входим в машинные состояния)
@dp.message_handler(commands='input_code', state=None)
async def start_input_code():
    await Form1.code_inp.set()


# выход из машинных состояний
@dp.message_handler(state="*", commands='Отменить ввод кода')
@dp.message_handler(Text(equals='Отменить ввод кода', ignore_case=True), state="*")
async def cancel_input_code(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отправка кода верификации отменена", reply_markup=keyboard_send_code)


# ловим код и записываем его в переменную
@dp.message_handler(state=Form1.code_inp)
async def input_code(message: types.Message, state: FSMContext):
    global code

    async with state.proxy() as data:
        data['code_inp'] = message.text
        code = str(data['code_inp'])
    num = len(code)

    # проверяем, правильное ли количество символов ввел пользователь, если да, то завершаем процесс ввода, если нет, то перенаправляем на ввод кода заново
    if num == 4:

        await message.reply('Отлично, код записан!\nПроверьте правильность введенных данных\nЕсли код записан верно, то нажми на "Отправить код"\nЕсли код записан неверно, то нажмите "Назад" ',
                            reply_markup=keyboard_send_code)
        await state.finish()
    else:
        await message.reply("Введен неверный код! Введите заново.")
        await start_input_code(message)


# отвечает на текст
@dp.message_handler()
async def text(message: types.Message):
    if message.text == 'Привет':
        await message.reply("И тебе привет!", reply_markup=keyboard_start)

    elif message.text == 'Стоп':
        beat_bot.stop_bot()
        await message.reply("Бот полностью остановлен!", reply_markup=keyboard_start)

    elif message.text == 'Назад':
        await message.reply('Вернулся назад!', reply_markup=keyboard_code_or_cookie)

    elif message.text == 'Начать всё заново':
        await message.reply("Начинаем всё заново!", reply_markup=keyboard_start)

    elif message.text == 'Начать авторизацию':
        await message.reply("Бот загружается")
        beat_bot.oauth_beatstars()
        await bot.send_message(message.from_user.id, "Бот запущен!", reply_markup=keyboard_send_data)

    elif message.text == 'Ввести данные для авторизации':
        await bot.send_message(message.from_user.id, "Введи имя пользователя", reply_markup=keyboard_input_data)
        await start_input_data()

    elif message.text == 'Отправить данные на сайт':
        await message.reply('Идёт отправка данных на сайт...')
        beat_bot.username_input()
        beat_bot.password_input()
        await bot.send_message(message.from_user.id, 'Отлично! Данные отправлены на сайт!\nТеперь нажми на кнопку "Войти" ')

    elif message.text == 'Войти':
        '''Нажимает на кнопку войти и проверяет, не было ли слишком много попыток входа'''

        await message.reply('Бот нажал на кнопку "Войти", подождите немного...')
        beat_bot.login_button()

        if sent_code == 'yes':
            await bot.send_message(message.from_user.id, 'Проверьте почту\nEсли вам пришел код, то жмите на "Ввести код"\nЕсли нет, то жми "Согласиться с куки"', reply_markup=keyboard_code_or_cookie)
        elif sent_code == 'not':


    elif message.text == 'Ввести код':
        await message.reply("Введи код подтверждения, пришедший на твою почту", reply_markup=keyboard_input_code)
        await start_input_code(message)

    elif message.text == 'Отправить код':
        '''Проводит проверку, есть ли этот элемент на сайте, если да, то отправляет код, если нет, то отправляет обратно'''

        beat_bot.send_code()

        if find_element == 1:
            await message.reply("Код отправлен! Теперь нужно согласиться с куки-файлами", reply_markup=keyboard_cookie)
        else:
            await message.reply('Код не отправлен, нажмите на кнопку "Войти" заново и введите правильный код верификации!', reply_markup=keyboard_send_data)

    elif message.text == 'Согласиться с куки':
        '''Проводит проверку, есть ли этот элемент на сайте, если да, то соглашается с куки, если нет, то отправляет обратно'''

        beat_bot.agree_to_cookies()

        if agree == 1:
            await message.reply("Бот согласился с куки!", reply_markup=keyboard_start_bot)
        else:
            await message.reply('Не получилось согласиться с куки!\n'
                                'Еще раз проверьте свою почту, если пришел код, то нажмите на "Ввести код"\n'
                                'Если кода нет, то попробуйте согласиться с куки позднее', reply_markup=keyboard_code_or_cookie)

    elif message.text == 'Запустить бота':
        beat_bot.start_bot()
        await message.reply("Бот запущен, можешь отдохнуть 😉", reply_markup=keyboard_start_bot)

    elif message.text == 'Запустить бота + репост твоих битов':
        await message.reply(
            'Бот запущен, сейчас он будет репостить твои биты\nА потом начнет слушать, комментировать, лайкать чужие биты\n'
            'А также, он будет подписываться на других пользователей! 😉')
        beat_bot.start_bot_with_reposts()

    elif message.text == 'Остановить бота':
        beat_bot.close_beatstars()
        await message.reply('Бот остановлен\nЧтобы запустить его заново, просто нажми на "Запустить бота" ', reply_markup=keyboard_start_bot)

    else:
        await message.reply("Что ты хотел?")


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    except Exception as ex:
        print(Fore.RED, ex)
