import ast

# define test expressions

formulas = [
    
"(2+1) / 5",

"""
if a>b:
    return b
"""

]

# print trees

for formula in formulas:

    tree = ast.parse(formula)
    print(ast.dump(tree,indent=2),"\n")


# define class that visits AST nodes
class v(ast.NodeVisitor):

    def __init__(self):
        self.tokens = []
        

    def f_continue(self, node):
        super(v, self).generic_visit(node)
    
    def visit_Compare(self,node):
        
        self.visit(node.left)
        
        for comparator in node.comparators:
            self.visit(comparator)
            
        for op in node.ops:
            self.visit(op)
            
    def visit_Return(self,node):
        self.f_continue(node)
        self.tokens.append("Return")
        
    def visit_Gt(self,node):
        self.tokens.append(">")
        self.f_continue(node)
        
    def visit_Lt(self,node):
        self.tokens.append(">")
        self.f_continue(node)
        
    def visit_If(self,node):
        self.f_continue(node)
        self.tokens.append("if")
        
    def visit_Add(self, node):
        self.tokens.append('+')
        self.f_continue(node)

    def visit_And(self, node):
        self.tokens.append('&&')
        self.f_continue(node)
    
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        self.visit(node.op)

    def visit_BoolOp(self, node):
        for val in node.values:
            self.visit(val)
        self.visit(node.op)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        self.visit(node.func)

    def visit_Div(self, node):
        self.tokens.append('/')
        self.f_continue(node)

    def visit_Expr(self, node):
        # print('visit_Expr')
        self.f_continue(node)

    def visit_Import(self, stmt_import):
        for alias in stmt_import.names:
            print('import name "%s"' % alias.name)
            print('import object %s' % alias)
        self.f_continue(stmt_import)

    def visit_Load(self, node):
        # print('visit_Load')
        self.f_continue(node)

    def visit_Module(self, node):
        # print('visit_Module')
        self.f_continue(node)

    def visit_Mult(self, node):
        self.tokens.append('*')
        self.f_continue(node)

    def visit_Name(self, node):
        self.tokens.append(node.id)
        self.f_continue(node)

    def visit_NameConstant(self, node):
        self.tokens.append(node.value)
        self.f_continue(node)

    def visit_Num(self, node):
        self.tokens.append(node.n)
        self.f_continue(node)

    def visit_Pow(self, node):
        self.tokens.append('pow')
        self.f_continue(node)

# generate postfix
for index, f in enumerate(formulas):
    visitor = v()
    visitor.visit(ast.parse(f))
    print(formulas[index],"\n----->",visitor.tokens)
