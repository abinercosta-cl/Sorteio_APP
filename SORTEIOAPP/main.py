# main.py
import database_setup # Importa seu script de setup
from ui import App
# Importa a classe principal da nossa interface
from ui import App

# Este é o ponto de entrada do programa.
# Ele cria uma instância da nossa janela e a exibe.
if __name__ == "__main__":
    database_setup.setup_database()
    app = App()
    app.mainloop()