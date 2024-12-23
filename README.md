# Ассемблер и интерпретатор для учебной виртуальной машины

## Описание
Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.
Форматом для файла-лога и файла-результата является yaml.

## Установка и запуск
1. Убедитесь, что у вас установлен Python 3.8 или выше.
2. Установите библиотеку pyyaml 
3. Установите зависимости Python:
   ```zsh
   pip install pyyaml
   ```
4. Скачайте проект или клонируйте репозиторий.
5. Создайте входной файл. Пример:
   ```
    LOAD_CONST 234, R84
    LOAD_MEM 667, R50
    STORE_MEM R109, 633
    SQRT R113, R71
   ```
6. Запустите проект:
   ```zsh
   python3 main.py
   ```

### Пример
```zsh
python3 main.py
```
### Результат работы программы
```yaml
memory_dump:
  start: 0
  end: 30
  data:
  - 0
  - 0
  - 0
  - 0
  - 0
  - 0
  - 0
  - 0
  - 0
  - 0
  - 4
  - 9
  - 16
  - 25
  - 36
  - 0
  - 0
  - 0
  - 0
  - 0
  - 2
  - 3
  - 4
  - 5
  - 6
  ```
В регистрах с адресами 10-14 находились исходные значения, в регистрах 20-24 - новые значения
## Тестирование
1. Для запуска тестов выполните:
   ```zsh
   python3 -m unittest tests.py
   ```
2. Убедитесь, что тестовые файлы находятся в рабочем каталоге.

## Скриншоты работы программы
![program.png](schreenshots/program.png)
![test.png](schreenshots/test.png)
---
