from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import pygame  # Для воспроизведения музыки
import os
import threading  # Для таймера
import time  # Для задержки
import sys  # Для завершения программы

class TrapMortgageCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super(TrapMortgageCalculator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Счетчик расчетов
        self.calculation_count = 0

        # Поля ввода
        self.add_widget(Label(text='Сума кридита (руб):'))
        self.loan_amount = TextInput(multiline=False, input_type='number')
        self.add_widget(self.loan_amount)

        self.add_widget(Label(text='Гадавая працентная ставка (%):'))
        self.interest_rate = TextInput(multiline=False, input_type='number')
        self.add_widget(self.interest_rate)

        self.add_widget(Label(text='Срок кридита (лет):'))
        self.loan_term = TextInput(multiline=False, input_type='number')
        self.add_widget(self.loan_term)

        # Кнопка расчета
        self.calculate_button = Button(text='Росчитать.')
        self.calculate_button.bind(on_press=self.calculate)
        self.add_widget(self.calculate_button)

        # Результат
        self.result_label = Label(text='Ежемесичный плотеж: ')
        self.add_widget(self.result_label)

        # Инициализация pygame для воспроизведения музыки
        pygame.init()

    def calculate(self, instance):
        if self.calculation_count >= 3:
            # Если расчетов уже 3, выводим "ловушку" и включаем музыку
            self.result_label.text = 'Ты такой дурачок, что даже не смог понять, что это ловушка. Так что получай: та-да-да-да-да-да-да!'
            self.calculate_button.disabled = True  # Отключаем кнопку

            # Воспроизведение музыки
            self.play_music("prodebila.mp3")

            # Запуск таймера на 33 секунды для завершения программы
            threading.Thread(target=self.shutdown_timer, args=(33,)).start()
            return

        try:
            # Получаем данные из полей ввода
            loan_amount = float(self.loan_amount.text)
            annual_interest_rate = float(self.interest_rate.text)
            loan_term_years = float(self.loan_term.text)

            # Проверка на корректность данных
            if loan_amount <= 0 or annual_interest_rate <= 0 or loan_term_years <= 0:
                self.result_label.text = 'Отрицательный кредит — это же так круто! Но невозможно.'
                return

            # Конвертируем годовые данные в месячные
            monthly_interest_rate = annual_interest_rate / 100 / 12
            loan_term_months = loan_term_years * 12

            # Расчет ежемесячного платежа
            if monthly_interest_rate == 0:  # Если процентная ставка 0%
                monthly_payment = loan_amount / loan_term_months
            else:
                numerator = loan_amount * monthly_interest_rate
                denominator = 1 - (1 + monthly_interest_rate) ** (-loan_term_months)
                monthly_payment = numerator / denominator

            # Выводим результат
            self.result_label.text = f'Ежемесичный плотёж: {monthly_payment:.2f} руб'
            self.calculation_count += 1  # Увеличиваем счетчик расчетов
        except ValueError:
            self.result_label.text = 'Это же надо быть гением, чтобы не суметь понять, что буквы нельзя делить!'

    def play_music(self, filename):
        # Проверяем, существует ли файл
        if os.path.exists(filename):
            # Загружаем и воспроизводим музыку
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        else:
            self.result_label.text = 'Ошибка: Файл с музыкой не найден!'

    def shutdown_timer(self, delay):
        # Ждем указанное количество секунд
        time.sleep(delay)
        # Завершаем программу
        os._exit(0)  # Аварийное завершение

class TrapMortgageApp(App):
    def build(self):
        return TrapMortgageCalculator()

if __name__ == '__main__':
    TrapMortgageApp().run()
