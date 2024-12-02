from dependency_visualizer import load_config, get_dependencies, collect_all_dependencies, generate_graph
import json

# Тестирование функции load_config
def test_load_config():
    mock_yaml_data = """
    visualization_path: "dot"
    repo_name: "test-package"
    output_file: "output_graph.dot"
    """
    with open('mock_config.yaml', 'w') as f:
        f.write(mock_yaml_data)

    config = load_config("mock_config.yaml")
    assert config["visualization_path"] == "dot", "Error in visualization_path"
    assert config["repo_name"] == "test-package", "Error in repo_name"
    assert config["output_file"] == "output_graph.dot", "Error in output_file"
    print("test_load_config passed")

# Тестирование функции get_dependencies
def test_get_dependencies():
    mock_package_json = {
        "dependencies": {
            "express": "4.17.1",
            "mongoose": "5.9.2"
        },
        "devDependencies": {
            "jest": "26.0.1"
        }
    }
    
    with open('mock_package.json', 'w') as f:
        f.write(json.dumps(mock_package_json))
    
    dependencies, dev_dependencies = get_dependencies('mock_package.json')
    
    assert dependencies == {"express": "4.17.1", "mongoose": "5.9.2"}, "Error in dependencies"
    assert dev_dependencies == {"jest": "26.0.1"}, "Error in devDependencies"
    print("test_get_dependencies passed")

# Тестирование функции collect_all_dependencies
def test_collect_all_dependencies():
    dependencies = {"express": "4.17.1", "mongoose": "5.9.2"}
    dev_dependencies = {"jest": "26.0.1"}
    
    all_deps = collect_all_dependencies(dependencies, dev_dependencies)
    
    assert "express" in all_deps, "express not in all_deps"
    assert "jest" in all_deps, "jest not in all_deps"
    assert all_deps["express"] == ("4.17.1", "solid"), "express dependency style mismatch"
    assert all_deps["jest"] == ("26.0.1", "dashed"), "jest dependency style mismatch"
    
    print("test_collect_all_dependencies passed")

# Тестирование функции generate_graph
def test_generate_graph():
    dependencies = {
        "express": ("4.17.1", "solid"),
        "mongoose": ("5.9.2", "solid"),
        "jest": ("26.0.1", "dashed")
    }
    
    expected_graph = (
        'digraph G {\n'
        '  "express" [label="express (4.17.1)"];\n'
        '  "express" -> "4.17.1" [style=solid];\n'
        '  "mongoose" [label="mongoose (5.9.2)"];\n'
        '  "mongoose" -> "5.9.2" [style=solid];\n'
        '  "jest" [label="jest (26.0.1)"];\n'
        '  "jest" -> "26.0.1" [style=dashed];\n'
        '}\n'
    )
    
    graph = generate_graph(dependencies)
    
    assert graph == expected_graph, "Graph generation mismatch"
    print("test_generate_graph passed")

# Запуск всех тестов
def run_tests():
    test_load_config()
    test_get_dependencies()
    test_collect_all_dependencies()
    test_generate_graph()

if __name__ == "__main__":
    run_tests()
