# (1) FUNCTION GetQuorum(Tree: NetworkHierarchy): QuorumSet;
# (2) VAR left, right: QuorumSet;
# (3) BEGIN
# (4) IF Empty (Tree) THEN
# (5) RETURN ({});
# (6) ELSE IF GrantsPermission(Tree↑.Node) THEN
# (7) RETURN((Tree↑.Node) ∪ GetQuorum (Tree↑.LeftChild));
# (8) OR
# (9) RETURN((Tree↑.Node) ∪ GetQuorum (Tree↑.RightChild));
# (10) ELSE
# (11) left←GetQuorum(Tree↑.left);
# (12) right←GetQuorum(Tree↑.right);
# (13) IF (left =∅ ∨ right = ∅) THEN
# (14) (* Unsuccessful in establishing a quorum *)
# (15) EXIT(-1);
# (16) ELSE
# (17) RETURN(left ∪ right);
# (18) END; (* IF *)
# (19) END; (* IF *)
# (20) END; (* IF *)
# (21) END GetQuorum

# Ok so I need Node class, whitch implements grantsPermissions

def getQuorum(tree):
    pass