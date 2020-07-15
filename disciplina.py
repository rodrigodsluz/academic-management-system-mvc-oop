# Importando bibliotecas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path


# ----Possíveis erros que vão ser tratados----

# Caso o código da disciplina seja inválido
class InvalidCode(Exception):
    pass


# Caso o nome seja inválido
class InvalidName(Exception):
    pass


# Caso tenha alguma informação repetida
class informationAlreadyExists(Exception):
    pass


# Caso tenha algum campo de preenchimento em branco 
class EmptyField(Exception):
    pass


# Classe do disciplina
class Disciplina:
    # Método construtor da disciplina
    def __init__(self, codigoDisciplina, nomeDisciplina, cargaHoraria):
        self.__codigoDisciplina = codigoDisciplina
        self.__nomeDisciplina = nomeDisciplina
        self.__cargaHoraria = cargaHoraria

    # ----Métodos Getters----
    def getCodigoDisciplina(self):
        return self.__codigoDisciplina

    def getNomeDisciplina(self):
        return self.__nomeDisciplina

    def getCargaHoraria(self):
        return self.__cargaHoraria


# Limite da tela de inserção da disciplina
class InsereDisciplinaView(tk.Toplevel):
    # Método construtor
    def __init__(self, control):
        tk.Toplevel.__init__(self)
        # Tamanho da janela
        self.geometry('350x300')
        # Cria o título
        self.title('Insira a disciplina')
        # Controle
        self.control = control

        # Criar as partes necessárias de pegar a código da disciplina
        self.frameCodigoDisciplina = tk.Frame(self)
        self.frameCodigoDisciplina.pack()
        self.labelCodigoDisciplina = tk.Label(
            self.frameCodigoDisciplina, text='Código:')
        self.labelCodigoDisciplina.pack(side='left')
        self.inputCodigoDisciplina = tk.Entry(
            self.frameCodigoDisciplina, width=20)
        self.inputCodigoDisciplina.pack(side='left')

        # Criar as partes necessárias de pegar a nome da disciplina
        self.frameNomeDisciplina = tk.Frame(self)
        self.frameNomeDisciplina.pack()
        self.labelNomeDisciplina = tk.Label(
            self.frameNomeDisciplina, text='Nome:')
        self.labelNomeDisciplina.pack(side='left')
        self.InputNomeDisciplina = tk.Entry(self.frameNomeDisciplina, width=20)
        self.InputNomeDisciplina.pack(side='left')

        # Criar as partes necessárias de pegar a carge horária da disciplina
        self.frameCargaH = tk.Frame(self)
        self.frameCargaH.pack()
        self.labelCargaH = tk.Label(self.frameCargaH, text='Carga horária:')
        self.labelCargaH.pack(side='left')
        self.chooseCombo = tk.StringVar()
        self.comboboxCargaH = ttk.Combobox(
            self.frameCargaH, width=20, textvariable=self.chooseCombo)
        self.comboboxCargaH.pack(side='left')
        # Lista para o combobox que faz aparecer essas opções
        self.cargasHorarias = ['32', '48', '64', '80', '96']
        self.comboboxCargaH['values'] = self.cargasHorarias

        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # --- Botões---
        # Botão para inserir disciplina
        self.buttonInsere = tk.Button(
            self.frameButton, text='Inserir', font=('Negrito', 11))
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind("<Button>", control.insereHandler)

        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(
            self.frameButton, text='Clear', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandler)

        # Botão para sair após inserir a disciplina
        self.buttonConcluido = tk.Button(
            self.frameButton, text='Concluído', font=('Negrito', 11))
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind("<Button>", control.concluidoHandler)

    # Método para mostrar mensagens de aviso para o usuário
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)


# Limite para mostrar as informações que já foram cadastradas
class MostraDisciplinasView():
    def __init__(self, str):
        messagebox.showinfo('Lista de disciplinas cadastradas', str)


# Classe controladora da disciplina
class CtrlDisciplina():
    # Método construtor
    def __init__(self, mainControl):
        # Passando como parâmetro controlador principal
        self.ctrlMain = mainControl

        # ---Ler as informações dos arquivos que foram salvos ---
        if not os.path.isfile("disciplina.pickle"):
            self.disciplinasList = []
        else:
            with open("disciplina.pickle", "rb") as f:
                self.disciplinasList = pickle.load(f)

    # Método para inserir a disciplina
    def insereDisciplina(self):
        self.limiteIns = InsereDisciplinaView(self)

    # Método handler para inserir, ele irá lidar com possíveis erros e cadastrar as disciplinas
    def insereHandler(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.InputNomeDisciplina.get()) == 0 or len(self.limiteIns.inputCodigoDisciplina.get()) == 0:
                raise EmptyField()

            # Verificando se já o existe o nome ou o código da disciplina
            for disc in self.disciplinasList:
                if disc.getNomeDisciplina() == self.limiteIns.InputNomeDisciplina.get() or disc.getCodigoDisciplina() == self.limiteIns.inputCodigoDisciplina.get():
                    raise informationAlreadyExists()

            # Verifica se o nome está inválido
            if len(self.limiteIns.InputNomeDisciplina.get()) < 5 or len(self.limiteIns.InputNomeDisciplina.get()) > 30 or not self.limiteIns.InputNomeDisciplina.get().replace(" ", "").isalpha():
                raise InvalidName()

            # Verifica se o código da disciplina é inválido
            if len(self.limiteIns.inputCodigoDisciplina.get()) != 6:
                raise InvalidCode()

        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'Por favor, preencha todos os campos!')

        # Mostra mensagem avisando o usuário sobre o erro
        except informationAlreadyExists:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', "Nome ou código da disciplina já existem!")

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidName:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "O nome está inválido! Exemplo válido: Computação Orientado a Objetos I")

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidCode:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "O código está inválido! Exemplo válido: COM220")

        else:
            # ---Caso não tenha erros cadastra o curso---
            codigo = self.limiteIns.inputCodigoDisciplina.get()
            nome = self.limiteIns.InputNomeDisciplina.get()
            cargaH = self.limiteIns.chooseCombo.get()
            # Instancia a disciplina
            disciplina = Disciplina(codigo, nome, cargaH)
            # Adiciona a disciplina instanciada na lista de disciplinas
            self.disciplinasList.append(disciplina)
            self.limiteIns.mostraJanela(
                'Parabéns, cadastro bem sucedido!', 'A disciplina foi cadastrada com sucesso!')

            # Limpa os campos preenchidos
            self.clearHandler(event)

    # Método para mostrar as disciplinas
    def mostraDisciplinas(self):
        if len(self.disciplinasList) != 0:
            str = 'Código -- Nome -- Carga Hor'
            str += '\n-------------------------------------\n'
            for disc in self.disciplinasList:
                str += f'{disc.getCodigoDisciplina()} -- {disc.getNomeDisciplina()} -- {disc.getCargaHoraria()}'
                str += '\n-------------------------------------\n'

        else:
            str = 'Não existem disciplinas cadastradas!'

        self.limiteMost = MostraDisciplinasView(str)

    # Método getter para pegar o objeto disciplina
    def getDisciplinaObj(self, codigoDisciplina):
        # Declara um objeto vazio
        objDisciplina = None
        # Se o código da disciplina passado como parâmetro é igual então ele retorna o objeto disciplina inteiro
        for disciplina in self.disciplinasList:
            if disciplina.getCodigoDisciplina() == codigoDisciplina:
                objDisciplina = disciplina
        return objDisciplina

    # Método getter para pegar a lista de disciplinas
    def getDisciplinasList(self):
        return self.disciplinasList

    # Método para limpar os campos de preenchimento que foram preenchidos
    def clearHandler(self, event):
        self.limiteIns.inputCodigoDisciplina.delete(
            0, len(self.limiteIns.inputCodigoDisciplina.get()))

        self.limiteIns.InputNomeDisciplina.delete(
            0, len(self.limiteIns.InputNomeDisciplina.get()))

        self.limiteIns.comboboxCargaH.delete(
            0, len(self.limiteIns.comboboxCargaH.get()))

    # Método para destruir a tela e sair
    def concluidoHandler(self, event):
        self.limiteIns.destroy()

    # Método para salvar todas as informações que foram registradas
    def saveDisciplinas(self):
        if len(self.disciplinasList) != 0:
            with open("disciplina.pickle", "wb") as f:
                pickle.dump(self.disciplinasList, f)
