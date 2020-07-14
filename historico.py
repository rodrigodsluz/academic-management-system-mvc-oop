# Importando bibliotecas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path
# Importando outras classes
import aluno as alu
import curso as cur
import disciplina as disc
import grade as gra


# ----Possíveis erros que vão ser tratados----
# Caso a matrícula do aluno buscado não exista
class MatriculaDoesntExists(Exception):
    pass


# Caso a matrícula seja inválida
class InvalidMatricula(Exception):
    pass


# Caso a nota seja inválida
class InvalidNota(Exception):
    pass


# Caso o ano seja inválido
class InvalidYear(Exception):
    pass


# Caso tenha algum campo de preenchimento em branco
class EmptyField(Exception):
    pass


# Classe do histórico
class Historico:
    # Método construtor da grade
    def __init__(self, alunoHistorico, notaHistorico, yearHistorico, semesterHistorico, ):
        self.__alunoHistorico = alunoHistorico
        self.__notaHistorico = notaHistorico
        self.__yearHistorico = yearHistorico
        self.__semesterHistorico = semesterHistorico

        # Lista para disciplinas do histórico do aluno
        self.__disciplinasHistorico = []

        # Lista com disciplinas eletivas
        self.__listDiscEletivas = []
        # Lista com disciplinas obrigatórias
        self.__listDiscObrigatorias = []

        # Inicializando variável da carga horária eletiva
        self.__cargaHorariaEletiva = 0

        # Inicializando variável da carga horária obrigatória
        self.__cargaHorariaObrigatoria = 0

        # Lista com o histórico dos alunos
        self.__historicoAluno = []

     # ----Metódos Getters e para adicionar nas listas----
    def getDisciplinasHistorico(self):
        return self.__disciplinasHistorico

    def addDisciplinasHistoricos(self, discipline):
        self.__disciplinasHistorico.append(discipline)

    def addHistoricoAluno(self, historico):
        self.__historicoAluno.append(historico)

    def getHistoricoAluno(self):
        return self.__historicoAluno

    # Método para adicionar disciplinas eletivas
    def addDiscEletiva(self, disciplina):

        self.__cargaHorariaEletiva += int(disciplina.getCargaHoraria())
        self.__listDiscEletivas.append(disciplina)

    # Método para adicionar disciplinas obrigatorias
    def addDiscObrigatoria(self, disciplina):

        self.__cargaHorariaObrigatoria += int(disciplina.getCargaHoraria())
        self.__listDiscObrigatorias.append(disciplina)

     # Método getter para carga horária eletiva
    def getCargaHorariaEletiva(self):
        return self.__cargaHorariaEletiva

    # Método getter para carga horária obrigatória
    def getCargaHorariaObrigatoria(self):
        return self.__cargaHorariaObrigatoria

    # ----Métodos Getters----

    def getAlunoHistorico(self):
        return self.__alunoHistorico

    def getNotaHistorico(self):
        return self.__notaHistorico

    def getYearHistorico(self):
        return self.__yearHistorico

    def getSemesterHistorico(self):
        return self.__semesterHistorico


# Limite da tela de busca do histórico
class searchHistoricoView(tk.Toplevel):
    # Método construtor
    def __init__(self, control):
        tk.Toplevel.__init__(self)
        # Tamanho da janela
        self.geometry('350x300')
        # Cria o título
        self.title('Buscar o aluno')
        # Controle
        self.control = control

        # Criar as partes necessárias de pegar a matrícula do aluno para poder consultar o histórico
        self.frameNroMatricHistorico = tk.Frame(self)
        self.frameNroMatricHistorico.pack()
        self.labelNroMatricHistorico = tk.Label(
            self.frameNroMatricHistorico, text='Matrícula:')
        self.labelNroMatricHistorico.pack(side='top')
        self.inputNroMatricHistorico = tk.Entry(
            self.frameNroMatricHistorico, width=20)
        self.inputNroMatricHistorico.pack(side='left')

        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # --- Botões---
        # Botão para buscar o aluno pela sua matrícula
        self.buttonSearch = tk.Button(
            self.frameButton, text='Search', font=('Negrito', 11))
        self.buttonSearch.pack(side='left')
        self.buttonSearch.bind("<Button>", control.searchHandler)

        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(
            self.frameButton, text='Clear', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandlerInicio)

        # Botão para sair
        self.buttonConcluido = tk.Button(
            self.frameButton, text='Concluído', font=('Negrito', 11))
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind("<Button>", control.concluidoHandler)

    # Método para mostrar mensagens de aviso para o usuário
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)


# Limite para mostrar a janela de inserção do histórico do aluno
class InsereHistoricoView(tk.Toplevel):
    # Método construtor
    def __init__(self, control, alunoHist, disciplinasList):
        tk.Toplevel.__init__(self)
        self.alunoHist = alunoHist
        # Tamanho da janela
        self.geometry('350x300')
        # Cria o título
        self.title('Insira o histórico')
        # Controle
        self.control = control

        # Cria uma label que vai mostrar qual o nome do aluno que vai ter o histórico inserido
        self.frameNameAluno = tk.Frame(self)
        self.frameNameAluno.pack()
        self.labelNameAluno = tk.Label(
            self.frameNameAluno, text=f'Nome do aluno:\n{alunoHist.getNomeAluno()}\n\n')
        self.labelNameAluno.pack(side='top')

        # Criar as partes necessárias de escolher a disciplina
        self.frameChooseDisciplina = tk.Frame(self)
        self.frameChooseDisciplina.pack()
        self.labelChooseDisciplina = tk.Label(
            self.frameChooseDisciplina, text='Disciplina:')
        self.labelChooseDisciplina.pack(side='top')
        # Criando combo para o usuário colocar a disciplina escolhida
        self.chooseCombo = tk.StringVar()
        self.inputChooseDisciplina = ttk.Combobox(
            self.frameChooseDisciplina, width=20, textvariable=self.chooseCombo)
        self.inputChooseDisciplina.pack(side='top')
        # Lista que vai pegar apenas os códigos das disciplinas para colocar no combo
        codigosDisciplinas = []
        for disc in disciplinasList:
            codigosDisciplinas.append(disc.getCodigoDisciplina())
        # Colocando lista de disciplinas no combo para o usuário escolher
        self.inputChooseDisciplina['values'] = codigosDisciplinas

        # Criar as partes necessárias de pegar o ano
        self.frameYearHistorico = tk.Frame(self)
        self.frameYearHistorico.pack()
        self.labelYearHistorico = tk.Label(
            self.frameYearHistorico, text='Ano:')
        self.labelYearHistorico.pack(side='top')
        self.inputYearHistorico = tk.Entry(self.frameYearHistorico, width=20)
        self.inputYearHistorico.pack(side='left')

        # Criar as partes necessárias de pegar o semestre
        self.frameSemesterHistorico = tk.Frame(self)
        self.frameSemesterHistorico.pack()
        self.labelSemesterHistorico = tk.Label(
            self.frameSemesterHistorico, text='Semestre:')
        self.labelSemesterHistorico.pack(side='top')
        self.chooseComboSemesterHistorico = tk.StringVar()
        self.comboboxSemesterHistorico = ttk.Combobox(
            self.frameSemesterHistorico, width=20, textvariable=self.chooseComboSemesterHistorico)
        self.comboboxSemesterHistorico.pack(side='left')
        # Lista para o combobox que faz aparecer essas opções
        listaSemest = ['1', '2']
        self.comboboxSemesterHistorico['values'] = listaSemest

        # Criar as partes necessárias de pegar a nota
        self.frameNotaHistorico = tk.Frame(self)
        self.frameNotaHistorico.pack()
        self.labelNotaHistorico = tk.Label(
            self.frameNotaHistorico, text='Nota:')
        self.labelNotaHistorico.pack(side='top')
        self.inputNotaHistorico = tk.Entry(self.frameNotaHistorico, width=20)
        self.inputNotaHistorico.pack(side='left')

        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # --- Botões---
        # Botão para inserir o histórico do aluno
        self.buttonInsere = tk.Button(
            self.frameButton, text='Inserir', font=('Negrito', 11))
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind("<Button>", control.insereHandler)

        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(
            self.frameButton, text='Clear', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandler)

        # Botão para sair após inserir o histórico do aluno
        self.buttonConcluido = tk.Button(
            self.frameButton, text='Concluído', font=('Negrito', 11))
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind(
            "<Button>", control.concluidoHistoricoHandler)


# Limite para mostrar as informações que já foram cadastradas
class MostraHistoricosView():
    def __init__(self, str):
        messagebox.showinfo('Lista de históricos cadastrados', str)


# Classe controladora do histórico
class CtrlHistorico():
    # Método construtor
    def __init__(self, mainControl):
        # Passando como parâmetro controlador principal
        self.ctrlMain = mainControl

        # ---Ler as informações dos arquivos que foram salvos ---
        if not os.path.isfile("historicos.pickle"):
            self.historicosList = []
        else:
            with open("historicos.pickle", "rb") as f:
                self.historicosList = pickle.load(f)

    # Método para inserir o histórico
    def insereHistorico(self):

        self.limiteIns = searchHistoricoView(self)

    # Método para buscar o aluno a partir de sua matrícula
    def searchHandler(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.inputNroMatricHistorico.get()) == 0:
                raise EmptyField()

            # Verifica se a matrícula está inválida
            if len(self.limiteIns.inputNroMatricHistorico.get()) < 4 or len(self.limiteIns.inputNroMatricHistorico.get()) > 5 or not self.limiteIns.inputNroMatricHistorico.get().isdigit():
                raise InvalidMatricula()

        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'Por favor, preencha todos os campos!')

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidMatricula:
            self.limiteIns.mostraJanela(
                "Cuidado, atenção!", "A matrícula está inválida! Exemplo válido: 1001")

        else:
            # ---Caso não tenha erros vai encontrar o aluno---
            alunoMatricula = self.limiteIns.inputNroMatricHistorico.get()
            # Vai pegar o objeto aluno a partir de sua matrícula
            alunoObj = self.ctrlMain.ctrlAluno.getAlunoObj(alunoMatricula)

            try:
                # Se o aluno objeto for None, significa que a matrícula inserida não existe
                if alunoObj == None:
                    raise MatriculaDoesntExists()

            # Mostra mensagem avisando o usuário sobre o erro
            except MatriculaDoesntExists:
                str = ('Não existe aluno com essa matrícula!')
                self.limiteIns.mostraJanela('Cuidado, atenção!', str)
                # Deleta o input da matrícula
                self.limiteIns.inputNroMatricHistorico.delete(
                    0, len(self.limiteIns.inputNroMatricHistorico.get()))
            else:
                # Lista com apenas a lista de disciplinas
                disciplinasList = self.ctrlMain.ctrlDisciplina.getDisciplinasList()

                # Chama o limite da inserção do histórico, passando como parâmetro o objeto aluno escolhido e a lista de disciplinas dele
            self.HistoricoView = InsereHistoricoView(
                self, alunoObj, disciplinasList)
            # Destrói o limite
            self.limiteIns.destroy()

    # Método handler para inserir, ele irá lidar com possíveis erros e cadastrar os históricos
    def insereHandler(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.HistoricoView.inputYearHistorico.get()) == 0 or len(self.HistoricoView.inputNotaHistorico.get()) == 0 or len(self.HistoricoView.chooseComboSemesterHistorico.get()) == 0 or len(self.HistoricoView.chooseCombo.get()) == 0:
                raise EmptyField()

            # Verificando se a nota está inválida. Precisa ser nota entre 0 e 10
            if float(self.HistoricoView.inputNotaHistorico.get()) < 0 or float(self.HistoricoView.inputNotaHistorico.get()) > 10:
                raise InvalidNota()

            # Verificando se tem o ano está inválido. Precisa estar entre 2012 e 2021
            if int(self.HistoricoView.inputYearHistorico.get()) > 2021 or int(self.HistoricoView.inputYearHistorico.get()) < 2012 or not self.HistoricoView.inputYearHistorico.get().isdigit():
                raise InvalidYear()

        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'Por favor, preencha todos os campos!')

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidNota:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'A nota é inválida! Precisa ser uma valor entre 0 e 10')
            self.HistoricoView.inputNotaHistorico.delete(
                0, len(self.HistoricoView.inputNotaHistorico.get()))

        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidYear:
            self.limiteIns.mostraJanela(
                'Cuidado, atenção!', 'O ano é inválido! Precisa estar entre 2012 a 2021!')
            self.HistoricoView.inputYearHistorico.delete(
                0, len(self.HistoricoView.inputYearHistorico.get()))

        else:
            # ---Caso não tenha erros o histórico vai ser inserido------

            # Pega o aluno
            aluno = self.HistoricoView.alunoHist

            # Pega o código da disciplina escolhida
            choseCodigoDisciplina = self.HistoricoView.chooseCombo.get()

            # Pega o objeto disciplina inteiro a partir do código escolhido da disciplina
            objDisciplina = self.ctrlMain.ctrlDisciplina.getDisciplinaObj(
                choseCodigoDisciplina)

            # Pega o valor do ano
            year = self.HistoricoView.inputYearHistorico.get()

            # Pega o semestre escolhido
            semester = self.HistoricoView.chooseComboSemesterHistorico.get()

            # Pega a nota escolhida
            nota = self.HistoricoView.inputNotaHistorico.get()

            # Instancia o histórico
            historico = Historico(aluno, nota, year, semester)

            # Adiciona o histórico
            historico.addHistoricoAluno(historico)

            historico.addDisciplinasHistoricos(objDisciplina)

            # # Declara um lista vazia para a lista de disciplinas da grade do aluno
            disciplinasGradeAlunoList = []

            # Pega a lista de disciplinas da grade do aluno e coloca nessa lista
            disciplinasGradeAlunoList = self.ctrlMain.ctrlAluno.getListDisciplinaGrade(
                aluno)

            # Verificação dentro da lista de disciplinas da grade do aluno
            for disc in disciplinasGradeAlunoList:
                # Se o código da disciplina é igual então quer dizer que essa é a grade do aluno
                if objDisciplina.getCodigoDisciplina() == disc.getCodigoDisciplina():
                    # Portanto, ela será adicionada na lista de disciplinas obrigatórias
                    historico.addDiscObrigatoria(objDisciplina)
                    break
                else:
                    # Senão, então ela é um disciplina eletiva e será adicionada na lista de disciplinas eletivas
                    historico.addDiscEletiva(objDisciplina)
                    break

            # Adiciona o histórico na lista de históricos
            self.historicosList.append(historico)

            self.limiteIns.mostraJanela(
                'Parabéns, inserção bem sucedida!', 'O histórico do aluno foi inserido com sucesso!')

            # Limpa os campos preenchidos
            self.clearHandler(event)

    # Método para mostrar as grades
    def mostraHistoricos(self):
        str = ''
        if len(self.historicosList) != 0:
            for his in self.historicosList:

                str += f'Histórico do aluno {his.getAlunoHistorico().getNomeAluno()}\n'
                str += 'Disciplina -- Ano/Semestre\n'

                str += f'{his.getDisciplinasHistorico()[-1].getNomeDisciplina()} -- {his.getYearHistorico()}.{his.getSemesterHistorico()}\n'

                str += f'Nota: {his.getNotaHistorico()} -- '
                str += 'APROVADO' if float(his.getNotaHistorico()
                                           ) >= 6 else 'REPROVADO'
                str += '\n------------------------------------\n'
                str += f'Carga horária de disciplinas obrigatórias: {his.getCargaHorariaObrigatoria()}\n'
                str += f'\nCarga horária de disciplinas eletivas {his.getCargaHorariaEletiva()}'
                str += '\n------------------------------------\n'

        else:
            str += 'Não existem históricos cadastradas!'
        self.limiteMost = MostraHistoricosView(str)

    # Método para limpar os campos de preenchimento que foram preenchidos na tela de inserção do histórico
    def clearHandler(self, event):
        self.HistoricoView.inputYearHistorico.delete(
            0, len(self.HistoricoView.inputYearHistorico.get()))
        self.HistoricoView.inputNotaHistorico.delete(
            0, len(self.HistoricoView.inputNotaHistorico.get()))

    # Método para limpar os campos de preenchimento que foram preenchidos na tela busca
    def clearHandlerInicio(self, event):
        self.limiteIns.inputNroMatricHistorico.delete(
            0, len(self.limiteIns.inputNroMatricHistorico.get()))

    # Método para destruir a tela de busca sair
    def concluidoHandler(self, event):
        self.limiteIns.destroy()

    # Método para destruir a tela de inserção do histórico e sair
    def concluidoHistoricoHandler(self, event):
        self.HistoricoView.destroy()

    # Método para salvar todas as informações que foram registradas
    def saveHistoricos(self):
        if len(self.historicosList) != 0:
            with open("historicos.pickle", "wb") as f:
                pickle.dump(self.historicosList, f)
