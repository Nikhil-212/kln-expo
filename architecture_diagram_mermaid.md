graph TB
    %% User
    User[👤 User] -->|HTTP Requests| MainApp

    %% Main Flask Application
    subgraph "Flask Application"
        MainApp[📄 app.py<br/>Main Entry Point<br/>- Flask app instance<br/>- spaCy NLP model<br/>- LegalDocumentProcessor<br/>- Blueprint registration]
    end

    %% Routes (Blueprints)
    subgraph "Routes (Blueprints)"
        AuthBP[🔐 auth_bp<br/>Authentication Routes<br/>- /auth/login<br/>- /auth/signup<br/>- /auth/logout]
        MainBP[🏠 main_bp<br/>Main Routes<br/>- /<br/>- /generate<br/>- /history]
        DocumentBP[📋 document_bp<br/>Document Routes<br/>- /document/form<br/>- /document/generate<br/>- /document/view]
    end

    %% Services
    subgraph "Services"
        Processor[⚙️ LegalDocumentProcessor<br/>Core Business Logic<br/>- Document classification<br/>- Entity extraction<br/>- Document generation<br/>- Template processing]
    end

    %% Models
    subgraph "Models"
        UserModel[👥 User Model<br/>User Management<br/>- get_user()<br/>- get_user_by_username()<br/>- add_user()]
    end

    %% Templates
    subgraph "Templates"
        HTMLTemplates[🌐 HTML Templates<br/>Jinja2 Templates<br/>- login.html<br/>- signup.html<br/>- generate.html<br/>- history.html<br/>- document_form.html]
        DocTemplates[📄 Document Templates<br/>Jinja2 Templates by Language<br/>- /en/rental_agreement.jinja2<br/>- /en/land_sale_deed.jinja2<br/>- /es/rental_agreement.jinja2<br/>- /hi/rental_agreement.jinja2]
    end

    %% Static Assets
    subgraph "Static Assets"
        CSSFiles[🎨 CSS Files<br/>style.css]
        JSFiles[💻 JavaScript Files<br/>- auth.js<br/>- voice_input.js]
    end

    %% Database
    subgraph "External Database"
        Supabase[(🗄️ Supabase<br/>Users Table<br/>History Table<br/>- User auth data<br/>- Document history)]
    end

    %% External Dependencies
    subgraph "External Dependencies"
        SpaCy[🧠 spaCy NLP<br/>Entity Extraction]
        Jinja2[🔧 Jinja2<br/>Template Rendering]
        PythonDocx[📝 python-docx<br/>DOCX Generation]
        ReportLab[📊 ReportLab<br/>PDF Generation]
    end

    %% Relationships
    MainApp -->|Registers| AuthBP
    MainApp -->|Registers| MainBP
    MainApp -->|Registers| DocumentBP
    MainApp -->|Uses| Processor
    MainApp -->|Uses| UserModel
    Processor -->|Reads| DocTemplates
    UserModel -->|Queries| Supabase
    AuthBP -->|Uses| UserModel
    DocumentBP -->|Uses| Processor
    MainBP -->|Renders| HTMLTemplates
    DocumentBP -->|Renders| HTMLTemplates
    HTMLTemplates -->|Includes| CSSFiles
    HTMLTemplates -->|Includes| JSFiles
    Processor -->|Uses| SpaCy
    Processor -->|Uses| Jinja2
    Processor -->|Uses| PythonDocx
    Processor -->|Uses| ReportLab

    %% Styling
    classDef flaskClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef routeClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef serviceClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef modelClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef templateClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef staticClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dbClass fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px
    classDef extClass fill:#f9fbe7,stroke:#827717,stroke-width:2px
    classDef userClass fill:#fff8e1,stroke:#f57f17,stroke-width:2px

    class MainApp flaskClass
    class AuthBP,MainBP,DocumentBP routeClass
    class Processor serviceClass
    class UserModel modelClass
    class HTMLTemplates,DocTemplates templateClass
    class CSSFiles,JSFiles staticClass
    class Supabase dbClass
    class SpaCy,Jinja2,PythonDocx,ReportLab extClass
    class User userClass
