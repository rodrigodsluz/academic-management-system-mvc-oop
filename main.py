# Importando biblioteca tkinter
import tkinter as tk
# Importando outras classes
import aluno as alu
import curso as cur
import grade as gra
import disciplina as disc
import historico as hist


# Limite principal que mostra o menu com as opções 
class MainView():
    # Método construtor com a raíz e o controle
    def __init__(self, root, control):
        self.control = control
        self.root = root

        # Criando menu
        self.menuBar = tk.Menu(self.root)

        # Configuração
        self.root.config(menu=self.menuBar)

        # -------Opções do menu-------
        # Criar a opção de aluno
        self.alunoMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Aluno", menu=self.alunoMenu)
        self.alunoMenu.add_command(
            label="Insere", command=self.control.insereAluno)
        self.alunoMenu.add_command(
            label="Mostra", command=self.control.mostraAlunos)

        # Criar a opção de curso
        self.cursoMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Curso", menu=self.cursoMenu)
        self.cursoMenu.add_command(
            label="Insere", command=self.control.insereCurso)
        self.cursoMenu.add_command(
            label="Mostra", command=self.control.mostraCursos)

        # Criar a opção de grade
        self.gradeMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Grade", menu=self.gradeMenu)
        self.gradeMenu.add_command(
            label="Insere", command=self.control.insereGrade)
        self.gradeMenu.add_command(
            label="Mostra", command=self.control.mostraGrades)

        # Criar a opção de disciplina
        self.disciplinaMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(
            label="Disciplina", menu=self.disciplinaMenu)
        self.disciplinaMenu.add_command(
            label="Insere", command=self.control.insereDisciplina)
        self.disciplinaMenu.add_command(
            label="Mostra", command=self.control.mostraDisciplinas)

        # Criar a opção de histórico
        self.historicoMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Histórico", menu=self.historicoMenu)
        self.historicoMenu.add_command(
            label="Insere", command=self.control.insereHistorico)
        self.historicoMenu.add_command(
            label="Mostra", command=self.control.mostraHistoricos)

        # Criar a opção para sair e salvar ou sair sem salvar
        self.exitMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Sair", menu=self.exitMenu)
        self.exitMenu.add_command(
            label="Salvar tudo", command=self.control.saveData)
        self.exitMenu.add_command(
            label="Sair sem salvar", command=self.control.exitWithoutSaving)


# Classe do controlador principal
class MainController():
    def __init__(self):
        self.root = tk.Tk()
        # Passa a raíz que cria a janela principal e si mesma como parâmetro para o limite principal
        self.limite = MainView(self.root, self)

        # Isso irá chamar todos os controladores das outras classes, fazendo com que tudo funcione
        self.ctrlAluno = alu.CtrlAluno(self)
        self.ctrlCurso = cur.CtrlCurso(self)
        self.ctrlGrade = gra.CtrlGrade(self)
        self.ctrlDisciplina = disc.CtrlDisciplina(self)
        self.ctrlHistorico = hist.CtrlHistorico(self)

        # Cria o título do sistema
        self.root.title("Sistema MVC de gestão acadêmica (POO)")
        # Tamanho da janela principal
        self.root.geometry('650x420')

        # Start the mainloop
        self.root.mainloop()

    # -----Metódos para inserir e mostrar----
    def insereAluno(self):
        self.ctrlAluno.insereAluno()

    def mostraAlunos(self):
        self.ctrlAluno.mostraAlunos()

    def insereCurso(self):
        self.ctrlCurso.insereCurso()

    def mostraCursos(self):
        self.ctrlCurso.mostraCursos()

    def insereGrade(self):
        self.ctrlGrade.insereGrade()

    def mostraGrades(self):
        self.ctrlGrade.mostraGrades()

    def insereDisciplina(self):
        self.ctrlDisciplina.insereDisciplina()

    def mostraDisciplinas(self):
        self.ctrlDisciplina.mostraDisciplinas()

    def insereHistorico(self):
        self.ctrlHistorico.insereHistorico()

    def mostraHistoricos(self):
        self.ctrlHistorico.mostraHistoricos()

    # ----Métodos para salvar e sair-----
    def saveData(self):
        self.ctrlAluno.saveAlunos()
        self.ctrlCurso.saveCursos()
        self.ctrlGrade.saveGrades()
        self.ctrlDisciplina.saveDisciplinas()
        self.ctrlHistorico.saveHistoricos()
        self.root.destroy()

    def exitWithoutSaving(self):
        self.root.destroy()


# Chamada do controlador principal que fará a aplicação rodar
if __name__ == '__main__':
    c = MainController()
