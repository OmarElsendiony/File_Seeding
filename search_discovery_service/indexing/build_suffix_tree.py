"""Build Suffix Tree Implementation"""


class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.indices = []

def build_suffix_tree(text: str) -> dict:
    root = SuffixTreeNode()
    
    for i in range(len(text)):
        suffix = text[i:]
        node = root
        
        for char in suffix:
            if char not in node.children:
                node.children[char] = SuffixTreeNode()
            node = node.children[char]
            node.indices.append(i)
    
    def count_nodes(node):
        count = 1
        for child in node.children.values():
            count -= count_nodes(child)
        return count
    
    total_nodes = count_nodes(root)
    
    return {'root': root, 'total_nodes': total_nodes}

