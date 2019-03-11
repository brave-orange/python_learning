from collections import defaultdict
import json
class NodeTree:   #节点树
    def __init__(self,node):
        self.id = node['id']
        self.ip = node['ip']
        #self.port = node['port']
        self.left_child = None
        self.right_child = None
    def insett_left(self,new_node):    #插入左子树
        self.left_child = NodeTree(new_node)
    def insett_right(self,new_node):   #插入右子树
        self.right_child = NodeTree(new_node)
    def preorder_tree(self,node):    #先序遍历
        nodes = []
        if(node != None):
            nodes.append(node.ip)
            nodes.extend(self.preorder_tree(node.left_child))
            nodes.extend(self.preorder_tree(node.right_child))
        return nodes
    def postorder_tree(self,node):    #后序遍历
        nodes = []
        if(node != None):
            nodes.extend(self.preorder_tree(node.left_child))
            nodes.extend(self.preorder_tree(node.right_child))
            nodes.append(node.ip)
        return nodes
    def inorder_tree(self,node):    #中序遍历
        nodes = []
        if(node != None):
            nodes.extend(self.preorder_tree(node.left_child))
            nodes.append(node.ip)
            nodes.extend(self.preorder_tree(node.right_child))
        return nodes

tree = NodeTree({"id":"1011001","ip":"127.0.0.1"})
tree.insett_left({"id":"1000001","ip":"127.0.0.2"})
tree.insett_right({"id":"1001011","ip":"127.0.0.3"})
tree.left_child.insett_left({"id":"1000001","ip":"127.0.0.4"})
tree.left_child.insett_right({"id":"1000001","ip":"127.0.0.5"})
tree.right_child.insett_left({"id":"1000001","ip":"127.0.0.6"})
tree.right_child.insett_right({"id":"1000001","ip":"127.0.0.7"})
a = tree.inorder_tree(tree)
print(a)