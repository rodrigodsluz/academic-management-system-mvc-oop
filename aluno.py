# Importando bibliotecas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path
# importando curso
import curso as cur


# ----Possíveis erros que vão ser tratados----

# Caso o nome seja inválido
class InvalidName(Exception):
    pass


# Caso a matrícula seja inválida
class InvalidMatricula(Exception):
    pass


# Caso tenha alguma informação repetida
class InformationAlreadyExists(Exception):
    pass


# Caso tenha algum campo de preenchimento em branco
class EmptyField(Exception):
    pass


# Classe do aluno
class Aluno:
    # Método construtor do aluno
    def __init__(self, nroMatric, nomeAluno, cursoAluno):
        self.__nroMatric = nroMatric
        self.__nomeAluno = nomeAluno
        self.__cursoAluno = cursoAluno

    # ----Métodos Getters----
    def getNroMatric(self):
        return self.__nroMatric

    def getNomeAluno(self):
        return self.__nomeAluno

    def getCursoAluno(self):
        return self.__cursoAluno


# Limite da tela de inserção do aluno
class InsereAlunoView(tk.Toplevel):
    # Método construtor
    def __init__(self, control, cursosList):
        tk.Toplevel.__init__(self)
        # Tamanho da janela
        self.geometry('350x300')
        # Cria o título
        self.title("Insira o aluno")
        # Controle
        self.control = control

        # Criar as partes necessárias de pegar a matrícula do aluno
        self.frameNroMatric = tk.Frame(self)
        self.frameNroMatric.pack()
        self.labelNroMatric = tk.Label(self.frameNroMatric, text=' Matrícula:')
        self.labelNroMatric.pack(side='left')
        self.inputNroMatric = tk.Entry(self.frameNroMatric, width=20)
        self.inputNroMatric.pack(side='left')

        # Criar as partes necessárias de pegar o nome do aluno
        self.frameNomeAluno = tk.Frame(self)
        self.frameNomeAluno.pack()
        self.labelNomeAluno = tk.Label(self.frameNomeAluno, text='Nome:')
        self.labelNomeAluno.pack(side='left')
        self.inputNomeAluno = tk.Entry(self.frameNomeAluno, width=20)
        self.inputNomeAluno.pack(side='left')

        # Criar as partes necessárias de escolher o curso do aluno
        self.frameCursoAluno = tk.Frame(self)
        self.frameCursoAluno.pack()
        self.labelCursoAluno = tk.Label(self.frameCursoAluno, text='Curso:')
        self.labelCursoAluno.pack(side='left')
        # Criando combo para o usuário colocar os cursos
        self.chooseCombo = tk.StringVar()
        self.inputCursoAluno = ttk.Combobox(self.frameCursoAluno, width=20)
        self.inputCursoAluno.pack(side='left')
        # Lista que vai pegar apenas os códigos dos cursos para colocar no combo
        codigosCurso = []
        for curso in cursosList:
            codigosCurso.append(curso.getCodigoCurso())
        # Colocando lista no combo para o usuário escolher
        self.inputCursoAluno['values'] = codigosCurso

        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # --- Botões---
        # Botão para inserir aluno
        self.buttonInserir = tk.Button(
            self.frameButton, text='Inserir', font=('Negrito', 11))
        self.buttonInserir.pack(side='left')
        self.buttonInserir.bind("<Button>", control.insereHandler)

        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(
            self.frameButton, text='Clear', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandler)

        # Botão para sair após inserir o aluno
        self.buttonConcluido = tk.Button(
            self.frameButton, text='Concuído', font=('Negrito', 11))
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind("<Button>", control.concluidoHandler)

    # Método para mostrar mensagens de aviso para o usuário
    def mostraJanela(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)


# Limite para mostrar as informações que já foram cadastradas
class MostraAlunoView(tk.Toplevel):
    def __init__(self, str):
        messagebox.showinfo('Lista de alunos cadastrados', str)


# Classe controladora do aluno
class CtrlAluno():
    # Método construtor
    def __init__(self, mainControl):
        # Passando como parâmetro controlador principal
        self.ctrlMain = mainControl

        # ---Ler as informações dos arquivos que foram salvos ---
        if not os.path.isfile("alunos.pickle"):
            self.alunosList = []
        else:
            with open("alunos.pickle", "rb") as f:
                self.alunosList = pickle.load(f)

    # Método para inserir o aluno
    def insereAluno(self):
        # Lista com apenas a lista de cursos do aluno
        cursosList = self.ctrlMain.ctrlCurso.getCursosList()
        # Chama o limite da inserção do aluno, passando como parâmetro a lista de cursos

        self.limiteIns = InsereAlunoView(self, cursosList)

    # Método handler para inserir, ele irá lidar com possíveis erros e cadastrar os alunos
    def insereHandler(self, event):
        try:

            # Veirificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.inputNroMatric.get()) == 0 or len(self.limiteIns.inputNomeAluno.get()) == 0 or len(self.limiteIns.inputCursoAluno.get()) == 0:
                raise EmptyField()

            # Verificando se já o existe o nome ou a matrícula
            for aluno in self.alunosList:
                if self.limiteIns.inputNomeAluno.get() == aluno.getNomeAluno() or self.limiteIns.inputNroMatric.get() == aluno.getNroMatric():
                    raise InformationAlreadyExists()

            # Verifica se o nome está inválido
            if len(self.limiteIns.inputNomeAluno.get()) < 3 or len(self.limiteIns.inputNomeAluno.get()) > 30 or not self.limiteIns.inputNomeAluno.get().replace(" ", "").isalpha():
                raise InvalidName()

            # Verifica se a matrícula está inválida
            if len(self.limiteIns.inputNroMatric.get()) < 4 or len(self.limiteIns.inputNroMatric.get()) > 5 or not self.limiteIns.inputNroMatric.get().isdigit():
                raise InvalidMatricula()

        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "Por favor, preencha todos os campos!")

        # Mostra mensagem avisando o usuário sobre o erro
        except InformationAlreadyExists:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "Este nome ou número de matrícula já está existe!")

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidName:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "O nome está inválido! Exemplo válido: Rodrigo Duarte")

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidMatricula:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "A matrícula está inválida! Exemplo válido: 1001")

        else:
            # ---Caso não tenha erros cadastra o aluno---
            nroMatric = self.limiteIns.inputNroMatric.get()
            nome = self.limiteIns.inputNomeAluno.get()
            curso = self.limiteIns.inputCursoAluno.get()
            # Instancia o aluno
            aluno = Aluno(nroMatric, nome, curso)
            # Adiciona o aluno instanciado na lista de alunos
            self.alunosList.append(aluno)
            self.limiteIns.mostraJanela(
                'Parabéns, perfeito!', 'O aluno foi cadastrado com sucesso!')

            # Limpa os campos preenchidos
            self.clearHandler(event)

    # Método para mostrar os alunos
    def mostraAlunos(self):
        if len(self.alunosList) != 0:
            str = "Nome -- Matrícula -- Curso\n"
            str += '------------------------------------\n'
            for aluno in self.alunosList:
                str += f'{aluno.getNomeAluno()} -- {aluno.getNroMatric()} -- {aluno.getCursoAluno()}'
                str += '\n------------------------------------\n'
        else:
            str = 'Não existem alunos cadastrados!'

        self.limiteLista = MostraAlunoView(str)

    # Método getter para pegar a lista de disciplina da grade do aluno
    def getListDisciplinaGrade(self, alunoHistorico):
        # Declara uma lista para as disciplinas da grade do aluno
        listDisciplinaGrade = []

        # Pega o objeto do curso do aluno que foi passado por parâmetro
        curso = self.ctrlMain.ctrlCurso.getCursoObj(
            alunoHistorico.getCursoAluno())

        # Pega o objeto da grade do curso do aluno
        grade = self.ctrlMain.ctrlGrade.getGradeObjByCurso(curso)

        # Lista com apenas a lista de grades
        gradesList = self.ctrlMain.ctrlGrade.getGradesList()

        # Se os códigos das grades forem iguais, então a lista de disciplinas da grade do aluno
        for grad in gradesList:
            if grade.getCodigoGrade() == grad.getCodigoGrade():
                listDisciplinaGrade = grad.getDisciplinasGradeList()

        return listDisciplinaGrade

    # Método getter para pegar o objeto aluno
    def getAlunoObj(self, matriculaHistorico):
        # Declara um objeto vazio
        objAluno = None
        # Se a matrícula passada como parâmetro é igual então ele retorna o objeto aluno inteiro para passar pro histórico
        for aluno in self.alunosList:
            if aluno.getNroMatric() == matriculaHistorico:
                objAluno = aluno
        return objAluno

    # Método para limpar os campos de preenchimento que foram preenchidos
    def clearHandler(self, event):
        self.limiteIns.inputNroMatric.delete(
            0, len(self.limiteIns.inputNroMatric.get()))

        self.limiteIns.inputNomeAluno.delete(
            0, len(self.limiteIns.inputNomeAluno.get()))

        self.limiteIns.inputCursoAluno.delete(
            0, len(self.limiteIns.inputCursoAluno.get()))

    # Método para destruir a tela e sair
    def concluidoHandler(self, event):
        self.limiteIns.destroy()

    # Método para salvar todas as informações que foram registradas
    def saveAlunos(self):
        if len(self.alunosList) != 0:
            with open("alunos.pickle", "wb") as f:
                pickle.dump(self.alunosList, f)
