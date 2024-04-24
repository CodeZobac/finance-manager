# Finance Manager

## Objetivo da aplicação:
O Finance Manager é uma aplicação web desenvolvida para ajudar os usuários a gerenciar suas finanças pessoais. Ele permite aos usuários registrar suas contas financeiras, despesas e passivos, fornecendo uma visão geral clara de sua situação financeira. Além disso, o aplicativo oferece recursos para definir metas de economia e visualizar dados financeiros em gráficos intuitivos.

## Justificação técnica da escolha da framework:
A escolha da framework Django para o desenvolvimento do Finance Manager foi baseada em diversos fatores:

1. **Produtividade:** Django oferece um conjunto abrangente de ferramentas e funcionalidades que permitem o desenvolvimento rápido de aplicativos web. A sua arquitetura baseada em modelos, visões e templates facilita a organização do código e a implementação de novos recursos.

2. **Segurança:** Django possui recursos integrados de segurança, incluindo proteção contra vulnerabilidades comuns da web, autenticação de usuários e proteção contra ataques de injeção de SQL e XSS. Isso garante que o Finance Manager seja uma aplicação segura para armazenar informações financeiras sensíveis dos usuários.

3. **Escalabilidade:** Django é altamente escalável e pode lidar com grandes volumes de tráfego e dados. Ele suporta a criação de aplicativos robustos que podem ser facilmente dimensionados à medida que o número de usuários e a complexidade do aplicativo aumentam.

## Processo de instalação:
Para executar o Finance Manager em seu ambiente local, siga as etapas abaixo:

1. Clone o repositório do Finance Manager em seu computador:

    ```
    git clone <https://github.com/CodeZobac/finance-manager>
    ```

2. Navegue até o diretório do projeto:

    ```
    cd finance-manager
    ```

4. Faça o build e execute o servidor de desenvolvimento do Django com o docker:

    ```
    docker-compose up --build
    ```

5. Acesse o aplicativo em seu navegador usando o seguinte URL:

    ```
    http://localhost:8000/
    ```

## Como utilizar a aplicação:
Após iniciar o servidor de desenvolvimento, você poderá acessar o Finance Manager no seu navegador. O aplicativo oferece as seguintes funcionalidades:

- Registro e login de usuários.
- Adição de contas financeiras e definição de metas de economia.
- Registro de despesas e passivos.
- Visualização de dados financeiros em gráficos interativos.
