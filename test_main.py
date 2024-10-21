import pytest

from main import Parser


@pytest.mark.parametrize(
    'arg, expected', [
        ('P{}3', 'Некорректный ввод, отсутствуют структурированные данные\n'),
        ('!#$%!!#(&(#', 'Некорректный ввод, присутствуют запрещенные символы\n'),
    ]
)
def test_wrong_input(capfd, arg, expected):
    Parser().load_yaml(arg)
    out, err = capfd.readouterr()
    assert out == expected


@pytest.mark.parametrize(
    'arg, expected', [
        ('abc: 1', '''{
    abc => 1
}
'''),
        ('''name: "Lark Parser"
version: 1.0
dependencies:
  - "lark"
  - "pyyaml"
nested:
  level1:
    level2: "deep"''',
         '''{
    name => "Lark Parser",
    version => 1.0,
    dependencies => '(
        "lark"
        "pyyaml"
    ),
    nested => {
        level1 => {
            level2 => "deep"
        }
    }
}
'''),

        ('''# Конфигурация веб-приложения
app:
  name: "Simple Web App"
  version: "1.0.0"
  port: 8080

# Настройки базы данных
database:
  host: "localhost"
  port: 5432
  name: "app_db"
  user: "db_user"
  password: "securepassword"

# Логирование
logging:
  level: "info"
  file: "/var/log/app.log"

# Внешние сервисы
external_services:
  - name: "Email Service"
    url: "https://email.example.com"
    api_key: "your-email-api-key"
  - name: "Payment Gateway"
    url: "https://payments.example.com"
    api_key: "your-payment-api-key"''',
         '''{
    app => {
        name => "Simple Web App",
        version => "1.0.0",
        port => 8080
    },
    database => {
        host => "localhost",
        port => 5432,
        name => "app_db",
        user => "db_user",
        password => "securepassword"
    },
    logging => {
        level => "info",
        file => "/var/log/app.log"
    },
    external_services => '(
        {
            name => "Email Service",
            url => "https://email.example.com",
            api_key => "your-email-api-key"
        }
        {
            name => "Payment Gateway",
            url => "https://payments.example.com",
            api_key => "your-payment-api-key"
        }
    )
}
'''),
    ]
)
def test_correct_input(arg, expected):
    p = Parser()
    p.rec_parse(p.load_yaml(arg), 0)
    assert p.s == expected
