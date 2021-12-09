//
//  Header.h
//  tuan7
//
//  Created by Phạm Nguyên on 02/12/2021.
//

#ifndef Header_h
#define Header_h

#include <iostream>
using namespace std;

struct node
{
    int key;
    node* left;
    node* right;
};

node* initialNode(int n)
{
    node* tmp=new node;
    tmp->key=n;
    tmp->left=NULL;
    tmp->right=NULL;
    return tmp;
}

void insert(node* &head,int x)
{
    if (head==NULL)
    {
        head=initialNode(x);
        return;
    }
    if (head->key==x) return;
    if (x>head->key) insert(head->right,x);
    if (x<head->key) insert(head->left,x);
   
}

void NLR(node* head)
{
    if (head==NULL) return;
    cout<<head->key<<" ";
    NLR(head->left);
    NLR(head->right);
}

void LNR(node* head)
{
    if (head==NULL) return;
    LNR(head->left);
    cout<<head->key<<" ";
    LNR(head->right);
}
void LRN(node* head)
{
    if (head==NULL) return;
    LNR(head->left);
    LNR(head->right);
    cout<<head->key<<" ";
}
int getHeight(node* root)
{
    if (root==NULL) return -1;
    int left=getHeight(root->left)+1;
    int right=getHeight(root->right)+1;
    return max(left,right);
}
void printAtLevel(node* root, int level)
{
    if (level==0 && root !=NULL)
    {
        cout<<root->key<<" ";
    } else
    {
        if (root != NULL)
            {
                printAtLevel(root->left, level - 1);
                printAtLevel(root->right, level - 1);
            }
    }
    
}
void levelOrder(node* root)
{
    int k=getHeight(root);
    for (int i=0;i<=k;i++)
    {
        printAtLevel(root, i);
    }
}

node* search(node* root, int x)
{
    if (root==NULL) return NULL;
    if (root->key==x) return root;
    if (x>root->key) return search(root->right, x);
        else
          return search(root->left,x);
}
int heightNode(node* root, int x)
{
    node* tmp=search(root, x);
    return getHeight(tmp);
}
int countNode(node* root)
{

    if (root==NULL) return 0;
    return countNode(root->left)+countNode(root->right)+1;
}
node* findMax(node* root)
{
    node* tmp=root;
    while (tmp && tmp->right!=NULL)
    {
        tmp=tmp->right;
    }
    return tmp;
}

node* findMin(node* root)
{
    node* tmp=root;
    while(tmp && tmp->left!=NULL)
    {
        tmp=tmp->left;
    }
    return tmp;
}
void Remove(node*& root, int x)
{
    if (x<root->key) Remove(root->left, x);
    else if (x>root->key) Remove(root->right, x);
    else
    {
        if (root->left==NULL && root->right==NULL)
        {
            delete root;
            root=NULL;
        }
        else if (root->left==NULL)
        {
            node* tmp=root;
            root=root->right;
            delete tmp;
        }
        else if (root->right==NULL)
        {
            node* tmp=root;
            root=root->left;
            delete tmp;
        }
        else
        {
            node* tmp=findMax(root->left);
            root->key=tmp->key;
            Remove(root->left, tmp->key);
        }
    }
}

bool isBST(node* root)
{
    if (root==NULL) return true;
    node* minRight=findMin(root->right);
    node* maxLeft=findMax(root->left);
    int k=root->key;
    if (root->left==NULL || root->right==NULL) return true;
    if (k>minRight->key || k<maxLeft->key) return false;
    return (isBST(root->left) && isBST(root->right));
}

void removeTree(node* &head)
{
    if (head==NULL) return;
    removeTree(head->left);
    removeTree(head->right);
    head=NULL;
    free(head);
}
#endif /* Header_h */
