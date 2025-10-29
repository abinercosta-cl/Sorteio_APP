# 🎁 SorteioApp (Desktop)

## ⚠️ Status Atual: Protótipo

Este projeto está atualmente em **fase de prototipagem**.

O objetivo desta versão é validar a ideia e testar as funcionalidades principais (cadastro, sorteio[cite_start], controle de papéis  e relatórios).

Esta versão **não é considerada estável** para uso em um ambiente de produção (pelo cliente final) e pode conter bugs ou funcionalidades incompletas.

---

Este é um aplicativo de desktop para gerenciamento de sorteios, ideal para eventos ou programas de rádio. Ele permite o cadastro de participantes, a realização de sorteios justos e o acompanhamento de um histórico de vencedores.

O aplicativo foi desenvolvido em Python com uma interface gráfica moderna usando CustomTkinter [cite_start]e armazena todos os dados localmente em um banco de dados SQLite [cite: 176-449].

## ✨ Funcionalidades Principais

* **Cadastro de Participantes:** Adiciona novos participantes com Nome, CPF e Telefone.
* **Controle de Papéis:**
    * [cite_start]**Locutor:** Pode cadastrar participantes e realizar sorteios .
    * [cite_start]**Admin:** Pode fazer tudo o que o locutor faz e também **excluir** participantes .
* [cite_start]**Regra de Sorteio:** Participantes só podem ser sorteados até **duas vezes** [cite: 1-173, 176-449].
* **Histórico:** Visualiza os últimos vencedores diretamente na tela de sorteio.
* **Relatórios:** Filtra e exibe todos os ganhadores de um mês/ano específico.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Gráfica (GUI):** CustomTkinter
* [cite_start]**Banco de Dados:** SQLite [cite: 176-449]
* [cite_start]**Empacotador:** PyInstaller [cite: 174-175, 448-449]

---

## 🚀 Como Executar (para Desenvolvedores)

Se você quiser rodar o projeto a partir do código-fonte:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/abinercosta-cl/Sorteio_APP.git](https://github.com/abinercosta-cl/Sorteio_APP.git)
    cd Sorteio_APP
    ```

2.  **Crie e ative um ambiente virtual (venv):**
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    # No Windows (PyInstaller precisa de Pillow para ícones)
    pip install customtkinter pyinstaller Pillow
    
    # No Linux/macOS
    pip install customtkinter pyinstaller
    ```

4.  **Configure o Banco de Dados:**
    Este comando cria o arquivo `sorteio.db` e adiciona os usuários padrão [cite: 1-173]:
    ```bash
    python database_setup.py
    ```

5.  **Execute o aplicativo:**
    ```bash
    python main.py
    ```

### 🔑 Logins Padrão

[cite_start]Após rodar o `database_setup.py` [cite: 1-173], os logins são:
* **Usuário:** `admin` | **Senha:** `senha123`
* **Usuário:** `locutor` | **Senha:** `locutor123`

---

## 📦 Como Gerar o Executável

[cite_start]Este projeto usa o PyInstaller e um arquivo `.spec` customizado [cite: 448-449] para gerar o executável.

1.  Siga todos os passos da seção "Como Executar".
2.  Rode o build:
    ```bash
    pyinstaller SorteioApp.spec
    ```
3.  O aplicativo completo e pronto para rodar estará na pasta `dist/SorteioApp`.
