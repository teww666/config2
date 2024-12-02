import yaml
import json
import os

# Функция для загрузки конфигурации из yaml
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Функция для извлечения зависимостей из package.json
def get_dependencies(package_json_path):
    with open(package_json_path, 'r') as file:
        package_data = json.load(file)
    
    # Возвращаем только dependencies и devDependencies
    dependencies = package_data.get('dependencies', {})
    dev_dependencies = package_data.get('devDependencies', {})
    
    return dependencies, dev_dependencies

# Функция для рекурсивного сбора всех зависимостей (включая транзитивные)
def collect_all_dependencies(dependencies, dev_dependencies):
    all_deps = {}

    # Функция для добавления зависимостей
    def add_dependencies(dep_dict, style='solid'):
        for dep, version in dep_dict.items():
            if dep not in all_deps:
                all_deps[dep] = version
                # Подаем зависимость с определенным стилем
                all_deps[dep] = (version, style)
    
    # Сначала добавляем основные и dev-зависимости
    add_dependencies(dependencies, style='solid')
    add_dependencies(dev_dependencies, style='dashed')

    return all_deps

# Функция для создания графа зависимостей в формате Graphviz
def generate_graph(dependencies):
    graph = "digraph G {\n"
    
    # Добавление зависимостей в граф
    for dep, (version, style) in dependencies.items():
        graph += f'  "{dep}" [label="{dep} ({version})"];\n'
        graph += f'  "{dep}" -> "{version}" [style={style}];\n'
    
    graph += "}\n"
    return graph

# Основная функция
def main(config_file, package_json_path):
    # Загрузка конфигурации
    config = load_config(config_file)
    
    # Извлечение зависимостей
    dependencies, dev_dependencies = get_dependencies(package_json_path)
    
    # Собираем все зависимости, включая транзитивные
    all_dependencies = collect_all_dependencies(dependencies, dev_dependencies)
    
    # Генерация кода графа
    graph = generate_graph(all_dependencies)
    
    # Выводим код графа на экран
    print(graph)

    # Сохранение кода графа в файл
    with open(config['output_file'], 'w') as file:
        file.write(graph)
    
    print(f"Граф зависимостей сохранен в {config['output_file']}")

# Запуск программы
if __name__ == "__main__":
    main("config.yaml", "package.json")

