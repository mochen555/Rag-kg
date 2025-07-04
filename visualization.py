import json
import networkx as nx
from jinja2 import Template
from pyvis.network import Network
from data_structures import Node
from config import VIS_CONFIG, FILE_PATHS

def collect_data(node):
    graph_data = {}
    stack = [node]
    while stack:
        current = stack.pop()
        if current.graph:
            entities = current.graph.entities
            relations = current.graph.relations
            
            nodes = [{
                'id': entity, 
                'label': entity, 
                'color': VIS_CONFIG["NODE_COLOR"],
                'size': VIS_CONFIG["NODE_SIZE"]
            } for entity in entities]
            
            edges = [{
                'from': source,
                'to': target,
                'label': edge,
                'color': VIS_CONFIG["EDGE_COLOR"],
                'arrows': 'to'
            } for (source, edge, target) in relations]
            
            graph_data[current.name] = {'nodes': nodes, 'edges': edges}
        stack.extend(current.get_children())
    return graph_data

def generate_html(node, output_path=None):
    if not output_path:
        output_path = FILE_PATHS["OUTPUT_HTML"]
    
    def build_tree(node):
        return {
            'id': node.name,
            'text': node.name,
            'children': [build_tree(c) for c in node.get_children()]
        }
    
    tree_json = json.dumps(build_tree(node))
    graph_data = json.dumps(collect_data(node))
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Knowledge Graph</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/jstree.min.js"></script>
        <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
            .container { display: flex; height: 100vh; }
            #tree { width: 300px; border-right: 1px solid #ccc; padding: 10px; overflow: auto; }
            #graph { flex: 1; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="tree"></div>
            <div id="graph"></div>
        </div>
        <script>
            $(document).ready(function() {
                $('#tree').jstree({
                    'core': {
                        'data': {{ tree_json|safe }},
                        'themes': { 'dots': false }
                    }
                }).on('select_node.jstree', function(e, data) {
                    const nodeId = data.node.id;
                    const graphData = {{ graph_data|safe }}[nodeId];
                    if (!graphData) return;
                    
                    if (window.network) window.network.destroy();
                    
                    const container = document.getElementById('graph');
                    const options = {
                        nodes: {
                            shape: 'box',
                            color: '#97C2FC',
                            margin: 10,
                            font: { size: 14 }
                        },
                        edges: {
                            arrows: 'to',
                            color: '#666',
                            font: { background: 'white' }
                        },
                        physics: {
                            stabilization: {
                                enabled: true,
                                iterations: 100
                            }
                        }
                    };
                    window.network = new vis.Network(
                        container,
                        { 
                            nodes: new vis.DataSet(graphData.nodes), 
                            edges: new vis.DataSet(graphData.edges) 
                        },
                        options
                    );
                });
                $('#tree').on('ready.jstree', function() {
                    $("#tree").jstree('select_node', 'ROOT');
                });
            });
        </script>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(Template(html_template).render(
            tree_json=tree_json,
            graph_data=graph_data
        ))