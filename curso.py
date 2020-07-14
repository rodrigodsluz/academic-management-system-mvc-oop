# Importando bibliotecas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path
# importando grade
import grade as gra


# ----Possíveis erros que vão ser tratados----
# Caso o nome seja inválido
class InvalidName(Exception):
    pass


# Caso o código do curso seja inválido
class InvalidCode(Exception):
    pass


# Caso tenha alguma informação repetida
class InformationAlreadyExists(Exception):
    pass


# Caso tenha algum campo de preenchimento em branco
class EmptyField(Exception):
    pass


# Classe do curso
class Curso:
    # Método construtor do curso
    def __init__(self, codigoCurso, nomeCurso, gradeCurso):
        self.__codigoCurso = codigoCurso
        self.__nomeCurso = nomeCurso
        self.__gradeCurso = gradeCurso

    # ----Métodos Getters----
    def getCodigoCurso(self):
        return self.__codigoCurso

    def getNomeCurso(self):
        return self.__nomeCurso

    def getGrade(self):
        return self.__gradeCurso


# Limite da tela de inserção do curso
class InsereCursosView(tk.Toplevel):
    # Método construtor
    def __init__(self, control, gradesList):
        tk.Toplevel.__init__(self)
        # Tamanho da janela
        self.geometry("350x300")
        # Cria o título
        self.title('Insira o curso')
        # Controle
        self.control = control

        # Criar as partes necessárias de pegar a código do curso
        self.frameCodigoCurso = tk.Frame(self)
        self.frameCodigoCurso.pack()
        self.labelCodigoCurso = tk.Label(
            self.frameCodigoCurso, text='Código:')
        self.labelCodigoCurso.pack(side='left')
        self.inputCodigoCurso = tk.Entry(self.frameCodigoCurso, width=20)
        self.inputCodigoCurso.pack(side='left')

        # Criar as partes necessárias de pegar a código do curso
        self.frameNomeCurso = tk.Frame(self)
        self.frameNomeCurso.pack()
        self.labelNomeCurso = tk.Label(self.frameNomeCurso, text='Nome:  ')
        self.labelNomeCurso.pack(side='left')
        self.inputNomeCurso = tk.Entry(self.frameNomeCurso, width=20)
        self.inputNomeCurso.pack(side='left')

        # Criar as partes necessárias de selecionar a grade escolhido para o curso
        self.frameCursoGrade = tk.Frame(self)
        self.frameCursoGrade.pack()
        self.labelCursoGrade = tk.Label(
            self.frameCursoGrade, text='Grade: ')
        self.labelCursoGrade.pack(side='left')
        # Criando combo para o usuário colocar a grade escolhida
        self.chooseCombo = tk.StringVar()
        self.inputCursoGrade = ttk.Combobox(
            self.frameCursoGrade, width=18, textvariable=self.chooseCombo)
        self.inputCursoGrade.pack(side='left')

        # Lista que vai pegar apenas os códigos das grades para colocar no combo
        codigosGrade = []
        for grade in gradesList:
            codigosGrade.append(grade.getCodigoGrade())
        # Colocando lista no combo para o usuário escolher
        self.inputCursoGrade['values'] = codigosGrade

        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # --- Botões---
        # Botão para inserir curso
        self.buttonInsere = tk.Button(
            self.frameButton, text='Inserir', font=('Negrito', 11))
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind("<Button>", control.insereHandler)

        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(
            self.frameButton, text='Clear', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandler)

        # Botão para sair após inserir o curso
        self.buttonConluido = tk.Button(
            self.frameButton, text='Concluído', font=('Negrito', 11))
        self.buttonConluido.pack(side='left')
        self.buttonConluido.bind("<Button>", control.concluidoHandler)

    # Método para mostrar mensagens de aviso para o usuário
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)


# Limite para mostrar as informações que já foram cadastradas
class MostraCursosView():
    def __init__(self, str):
        messagebox.showinfo('Lista de cursos cadastrados', str)


# Classe controladora do curso
class CtrlCurso():
    # Método construtor
    def __init__(self, mainControl):
        # Passando como parâmetro controlador principal
        self.ctrlMain = mainControl

        # ---Ler as informações dos arquivos que foram salvos ---
        if not os.path.isfile("cursos.pickle"):
            self.cursosList = []
        else:
            with open("cursos.pickle", "rb") as f:
                self.cursosList = pickle.load(f)

    # Método para inserir o curso
    def insereCurso(self):
        # Lista com apenas a lista de grade dos cursos
        gradesList = self.ctrlMain.ctrlGrade.getGradesList()
        # Chama o limite da inserção do curso, passando como parâmetro a lista de grades
        self.limiteIns = InsereCursosView(self, gradesList)

    # Método handler para inserir, ele irá lidar com possíveis erros e cadastrar os cursos
    def insereHandler(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.inputNomeCurso.get()) == 0 or len(self.limiteIns.inputCodigoCurso.get()) == 0 or len(self.limiteIns.chooseCombo.get()) == 0:
                raise EmptyField()

            # Verificando se já o existe o nome ou o código do curso
            for curso in self.cursosList:
                if curso.getNomeCurso() == self.limiteIns.inputNomeCurso.get() or curso.getCodigoCurso() == self.limiteIns.inputCodigoCurso.get():
                    raise InformationAlreadyExists()

            # Verifica se o nome está inválido
            if len(self.limiteIns.inputNomeCurso.get()) < 5 or len(self.limiteIns.inputNomeCurso.get()) > 30 or not self.limiteIns.inputNomeCurso.get().replace(" ", "").isalpha():
                raise InvalidName()

            # Verifica se o código do curso é inválido
            if len(self.limiteIns.inputCodigoCurso.get()) != 3 or not self.limiteIns.inputCodigoCurso.get().replace(" ", "").isalpha():
                raise InvalidCode()

        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'Por favor, preencha todos os campos!')

        # Mostra mensagem avisando o usuário sobre o erro
        except InformationAlreadyExists:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'Nome ou código do curso já existe!')

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidName:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "O nome está inválido! Exemplo válido: Sistemas de Informação")

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidCode:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "O código está inválido! Exemplo válido: SIN")

        else:
            # ---Caso não tenha erros cadastra o curso---
            codigo = self.limiteIns.inputCodigoCurso.get()
            nome = self.limiteIns.inputNomeCurso.get()
            gradeComboCodigo = self.limiteIns.chooseCombo.get()
            # Passa o código da grade por parâmetro para retornar o objeto da grade
            grade = self.ctrlMain.ctrlGrade.getGradeObj(gradeComboCodigo)
            # Instancia o curso
            curso = Curso(codigo, nome, grade)
            # Adiciona o curso instanciado na lista de cursos
            self.cursosList.append(curso)
            self.limiteIns.mostraJanela(
                'Parabéns, curso inserido!', 'O curso foi cadastrado com sucesso!')

            # Limpa os campos preenchidos
            self.clearHandler(event)

    # Método para mostrar os cursos
    def mostraCursos(self):
        if len(self.cursosList) != 0:
            gradesList = self.ctrlMain.ctrlGrade.getGradesList()
            str = ''
            for curso in self.cursosList:
                str += 'Código -- Nome\n'
                str += '------------------------------------\n'
                str += f'{curso.getCodigoCurso()} -- {curso.getNomeCurso()}'
                str += '\n------------------------------------\n'
                for grade in gradesList:
                    if grade.getCodigoGrade() == curso.getGrade():
                        str += "Grade -- Ano/semestre\n"
                        str += f'{grade.getCodigoGrade()} -- {grade.getAno()}.{grade.getSemestre()}'
                        str += '\n------------------------------------\n'

        else:
            str = 'Não existem cursos cadastrados'

        self.limiteMost = MostraCursosView(str)

    # Método getter para pegar a lista de cursos
    def getCursosList(self):
        return self.cursosList

    # Método getter para pegar o objeto curso
    def getCursoObj(self, codigoCurso):
        # Declara um objeto vazio
        objCurso = None
        # Se a código passado como parâmetro é igual então ele retorna o objeto curso inteiro
        for curso in self.cursosList:
            if codigoCurso == curso.getCodigoCurso():
                objCurso = curso
        return objCurso

    # Método para limpar os campos de preenchimento que foram preenchidos
    def clearHandler(self, event):
        self.limiteIns.inputCodigoCurso.delete(
            0, len(self.limiteIns.inputCodigoCurso.get()))
        self.limiteIns.inputNomeCurso.delete(
            0, len(self.limiteIns.inputNomeCurso.get()))

    # Método para destruir a tela e sair
    def concluidoHandler(self, event):
        self.limiteIns.destroy()

    # Método para salvar todas as informações que foram registradas
    def saveCursos(self):
        if len(self.cursosList) != 0:
            with open("cursos.pickle", "wb") as f:
                pickle.dump(self.cursosList, f)
