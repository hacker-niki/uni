#include <bits/stdc++.h>

using namespace std;

struct Node {
    std::string value;
    int key;
    int height;
    Node *left = nullptr;
    Node *right = nullptr;

    explicit Node(int k) : key(k), height(1) {}

    Node(int k, const std::string &text) : key(k), height(1), value(text) {}

    Node(int k, int h) : key(k), height(h) {}
};

int height(Node *n) {
    if (n)
        return n->height;
    return 0;
}

void fix_height(Node *p) {
    int hl = height(p->left);
    int hr = height(p->right);
    p->height = (hl > hr ? hl : hr) + 1;
}

Node *rotate_right(Node *p) {
    Node *q = p->left;
    p->left = q->right;
    q->right = p;
    fix_height(p);
    fix_height(q);
    return q;
}

Node *rotate_left(Node *p) {
    Node *q = p->right;
    p->right = q->left;
    q->left = p;
    fix_height(p);
    fix_height(q);
    return q;
}

int balance_factor(Node *p) {
    return height(p->right) - height(p->left);
}

Node *balance(Node *p) {
    fix_height(p);
    if (balance_factor(p) >= 2) {
        if (balance_factor(p->right) < 0)
            p->right = rotate_right(p->right);
        return rotate_left(p);
    }
    if (balance_factor(p) <= -2) {
        if (balance_factor(p->left) > 0)
            p->left = rotate_left(p->left);
        return rotate_right(p);
    }
    return p;
}

Node *insert(Node *p, int key, const std::string &text) {
    if (!p)
        return new Node(key, text);
    if (key < p->key)
        p->left = insert(p->left, key, text);
    else
        p->right = insert(p->right, key, text);

    return balance(p);
}

void out(Node *p) {
    if (p->left)
        out(p->left);
    std::cout << p->value << ' ';
    if (p->right)
        out(p->right);
}

Node *left(Node *l) {
    if (l->left) {
        return left(l->left);
    }
    return l;
}

Node *right(Node *r) {
    if (r->right) {
        return right(r->right);
    }
    return r;
}

void swapNodes(Node *r) {
    std::swap(left(r)->value, right(r)->value);
}


void bfsAndGenerateGraphviz(Node *root, const std::string &filename) {
    if (!root) return;

    std::queue<Node *> q;
    q.push(root);

    std::ofstream file(filename);
    file << "digraph tree {\n";

    while (!q.empty()) {
        Node *current = q.front();
        q.pop();

        if (current->left) {
            file << "    " << current->key << " -> " << current->left->key << ";\n";
            q.push(current->left);
        }

        if (current->right) {
            file << "    " << current->key << " -> " << current->right->key << ";\n";
            q.push(current->right);
        }
    }

    file << "}\n";
    file.close();
}


int main() {
    Node *root = nullptr;
    root = insert(root, 10, "Ten");
    root = insert(root, 20, "Twenty");
    root = insert(root, 30, "Thirty");
    root = insert(root, 40, "Forty");
    root = insert(root, 50, "Fifty");
    root = insert(root, 25, "Twenty Five");
    root = insert(root, 11, "Ten");
    root = insert(root, 21, "Twenty");
    root = insert(root, 31, "Thirty");
    root = insert(root, 41, "Forty");
    root = insert(root, 51, "Fifty");
    root = insert(root, 26, "Twenty Five");
    root = insert(root, 12, "Ten");
    root = insert(root, 22, "Twenty");
    root = insert(root, 32, "Thirty");
    root = insert(root, 42, "Forty");
    root = insert(root, 52, "Fifty");
    root = insert(root, 27, "Twenty Five");

    bfsAndGenerateGraphviz(root, "tree.dot");

    std::cout << "Graphviz file generated: tree.dot" << std::endl;

    return 0;
}