from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext


# ||========================= Системи числення =========================||
class CONVERTER:
    """
    CONVERTER converts from one number system to other
    """
    def __init__(self, numeric, with_st, in_st):
        """
        CONVERTER converts from one number system to other
        :param numeric: ( 0-f )
        :param with_st: ( 2-10, 16 ) [with]
        :param in_st: ( 2-10, 16 ) [in]
        """
        self.system = {2: '0b', 3: '0t', 4: '0f', 5: '0i', 6: '0s', 7: '0v', 8: '0o', 9: '0n', 10: '0d', 16: '0x'}
        self.numeric = numeric
        self.with_st = with_st
        self.in_st = in_st

    # ----- З інших в десяткові -----
    def __multiply(self):
        """Converts from other systems to decimal.
        :return: numeric in decimal
        """
        alphabet = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
        numeric = self.numeric
        st = self.with_st
        system = self.system
        result = 0
        lin = []
        if st in system:
            numeric = str(numeric)
            for i in numeric:
                if i in alphabet:
                    i = alphabet.get(i)
                    lin.append(i)
                else:
                    i = int(i)
                    lin.append(i)
            lin.reverse()
            for j in range(0, len(lin)):
                result += lin[j] * (st ** j)
            result = system.get(self.in_st) + f'{result}'
            return result[2:]
        else:
            return '!!! Помилка у "st" !!!'
    # -------------------------------

    # ----- З десяккової в інші -----
    #   {numb} |{st}
    # ¯ {mn}   |———
    #   ————   |{div}
    #   {k}      {whole} = int(div)
    def __divide(self):
        """Converts from decimal to other systems.
        :return: numeric in st
        """
        alphabet = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
        numeric = self.numeric
        st = self.in_st
        system = self.system
        lin = []
        lst = system.get(st)
        res = int(numeric)
        if st in system:
            while res != 0:
                numb = res      # {numb}
                res = res / st  # {div}    ▲
                res = int(res)  # {whole}  |
                mn = st * res   # {mn}     |
                k = numb - mn   # {k}
                lin.append(k)
            lin.reverse()
            for i in lin:
                if i in alphabet:
                    lst += str(alphabet.get(i))
                else:
                    lst += str(i)
            return lst[2:]
        else:
            return '!!! Помилка у "st" !!!'
    # -------------------------------

    def convert(self):
        if self.with_st == self.in_st:
            return self.numeric
        elif self.with_st == 10:
            result = self.__divide()
            return result
        elif self.in_st == 10:
            result = self.__multiply()
            return result
        else:
            self.numeric = self.__multiply()
            result = self.__divide()
            return result
# ||====================================================================||


# |=== Операції ===|
def clear():    # Очистка полів воду і виводу
    txt_1.delete('1.0', END)
    txt_2.configure(state='normal')
    txt_2.delete('1.0', END)
    txt_2.configure(state='disable')


def delete():    # Очистка поля виводу
    txt_2.configure(state='normal')
    txt_2.delete('1.0', END)
    txt_2.configure(state='disable')


class OPERATIONS:
    def __init__(self):
        self.systems = {'=== (2) ===': 2, '=== (3) ===': 3, '=== (4) ===': 4, '=== (5) ===': 5, '=== (6) ===': 6,
                        '=== (7) ===': 7, '=== (8) ===': 8, '=== (9) ===': 9, '=== (10) ===': 10, '=== (16) ===': 16}
        self.alphabet = '0123456789abcdef'
        self.trigger = None
        self.value = ''      # ◥
        self.with_sys = ''    # | Заповнюєтся у іншій фукції
        self.in_sys = ''     # ◢

    @staticmethod
    def __message(mes, mark=False):
        """Output of messages.
        "mark" = "False": to display error messages
        "mark" = "True": to display the result
        :param mes: message
        :param mark: False / True
        """
        mes = str(mes)
        delete()
        if mark is False:
            txt_2.configure(state='normal')
            txt_2.insert(INSERT, mes)
            txt_2.configure(state='disable')
        elif mark is True:
            txt_2.configure(state='normal')
            txt_2.insert(INSERT, f'{mes}\n')
            txt_2.configure(state='disable')
        else:
            txt_2.configure(state='normal')
            txt_2.insert(INSERT, '''!!! Неправильно вказаний "mark" !!!
У методі "__message(mes, mark=False)" класа CONVERT''')
            txt_2.configure(state='disable')

    def __audit(self):
        lin = []
        st = self.systems.get(self.with_sys)
        for i in self.value:
            if i in self.alphabet[:st]:
                lin.append(True)
            else:
                lin.append(False)
        if False in lin:
            self.trigger = False
        else:
            self.trigger = True

    def function(self):
        self.value = txt_1.get('1.0', END)
        self.with_sys = combo_1.get()
        self.in_sys = combo_2.get()
        if self.with_sys != '' and self.in_sys != '' and self.value != '\n':
            if self.with_sys in self.systems and self.in_sys in self.systems:
                self.value = str(self.value)[:-1]
                self.__audit()
                if self.trigger is True:
                    self.with_sys = self.systems[self.with_sys]
                    self.in_sys = self.systems[self.in_sys]
                    result = CONVERTER(self.value, self.with_sys, self.in_sys).convert()
                    self.__message(result, True)
                else:
                    self.__message('''!!! Помилка !!!
[ Не відповідність системі ]\n''')
            else:
                self.__message('''!!! Помилка !!!
[ Неправильна система! ]\n''')
        else:
            self.__message('''!!! Помилка !!!
[ Певне вікно не заповнене! ]\n''')
# |================|


# |=== Налаштування вікна ===|
root = Tk()
root.title('[ Engineering calculator ]')
root.geometry(f'655x355')   # 470 / 700 || 1410 / 700
root['bg'] = '#1469C8'
root.resizable(width=False, height=False)
# |==========================|


# |=== Створення об'єктів ===|
# ----- Текст -----
lbl_1 = Label(root, text='SYSTEM 1', font=("Calibri Bold", 20), bg='#1469C8', fg='white')
lbl_1.grid(column=0, row=0)
lbl_2 = Label(root, text='SYSTEM 2', font=("Calibri Bold", 20), bg='#1469C8', fg='white')
lbl_2.grid(column=2, row=0)
# -----------------

# ----- Комбіновані списоки -----
combo_1 = Combobox(root, font=('Arial', 15))
combo_1['values'] = ('=== (2) ===', '=== (3) ===', '=== (4) ===', '=== (5) ===', '=== (6) ===', '=== (7) ===',
                     '=== (8) ===', '=== (9) ===', '=== (10) ===', '=== (16) ===')
combo_1.grid(column=0, row=1, padx=30, pady=30)
combo_2 = Combobox(root, font=('Arial', 15))
combo_2['values'] = ('=== (2) ===', '=== (3) ===', '=== (4) ===', '=== (5) ===', '=== (6) ===', '=== (7) ===',
                     '=== (8) ===', '=== (9) ===', '=== (10) ===', '=== (16) ===')
combo_2.grid(column=2, row=1, padx=30, pady=30)
# -------------------------------

# ----- Поля воду -----
txt_1 = scrolledtext.ScrolledText(root, width=30, height=8)
txt_1.grid(column=0, row=2)
txt_2 = scrolledtext.ScrolledText(root, state='disabled', width=30, height=8)
txt_2.grid(column=2, row=2)
# ---------------------

# ----- Стрілки -----
arrow_1 = Label(root, text=' --> ', font=("Calibri Bold", 20), bg='#1469C8', fg='white')
arrow_1.grid(column=1, row=1)
arrow_2 = Label(root, text=' --> ', font=("Calibri Bold", 20), bg='#1469C8', fg='white')
arrow_2.grid(column=1, row=2, pady=30)
# -------------------

# ------ Кнопки -----
btn_1 = Button(root, text="Convert", font=("Calibri", 15), bd=5, command=OPERATIONS().function)
btn_1.grid(column=0, row=3, padx=50, pady=25, stick='wens')
btn_2 = Button(root, text=" Clr ", font=("Calibri", 15), bd=5, command=clear)
btn_2.grid(column=1, row=3, pady=25, stick='wens')
btn_3 = Button(root, text="Del", font=("Calibri", 15), bd=5, command=delete)
btn_3.grid(column=2, row=3, padx=50, pady=25, stick='wens')
# -------------------
# |==========================|

root.mainloop()