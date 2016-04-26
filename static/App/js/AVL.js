function Node(key, data){
	return {
		key : key, // y-coordinate
		left : undefined,
		right : undefined,
		height : 1,
		data : data // stroke and segment information index
	}
}

function AVL(){
	var self = {};

	var _root = undefined;

	var LEFT_DIRECTION = -1;
	var NO_DIRECTION = 0;
	var RIGHT_DIRECTION = 1;
	
	function height(node){
		if (node === undefined){
			return 0;
		}
		return node.height;
	}

	function rightRotate(y){
		x = y.left;
		T2 = x.right;

		// Perform rotation
		x.right = y;
		y.left = T2;

		// Update heights
		y.height = Math.max(height(y.left), height(y.right)) + 1;
		x.height = Math.max(height(x.left), height(x.right)) + 1;

		return x;
	}

	function leftRotate(x){
		y = x.right;
		T2 = y.left;

		// Perform rotation
		y.left = x;
		x.right = T2;

		// Update heights
		x.height = Math.max(height(x.left), height(x.right)) + 1;
		y.height = Math.max(height(y.left), height(y.right)) + 1;

		return y;
	}

	function getBalance(node){
		if (node === undefined){
			return 0;
		}
		return height(node.left) - height(node.right);
	}

	function insertRecursively(node, key, data){
		// Perform the normal BST rotation
		if (node === undefined){
			return Node(key, data);
		}

		if (key < node.key){
			node.left = insertRecursively(node.left, key, data)
		}
		else {
			node.right = insertRecursively(node.right, key, data);
		}

		// Update height of this ancestor node
		node.height = Math.max(height(node.left), height(node.right)) + 1;

		// Get the balance factor of this ancestor node to check whether
		// this node became unbalanced
		var balance = getBalance(node);

		// If this node becomes unbalanced, then there are 4 cases
		// Left Left case
		if (balance > 1 && key < node.left.key){
			return rightRotate(node);
		}

		// Right Right case
		if (balance < -1 && key > node.right.key){
			return leftRotate(node);
		}

		// Left Right case
		if (balance > 1 && key > node.left.key){
			node.left = leftRotate(node.left);
			return rightRotate(node);
		}

		// Right Left case
		if (balance < -1 && key < node.right.key){
			node.right = rightRotate(node.right);
			return leftRotate(node);
		}

		return node;
	}

	self.insert = function(key, data){
		_root = insertRecursively(_root, key, data, undefined, 0);
	}

	self.preOrder = function(node){
		if (node !== undefined){
			console.log(node.key + " ");
			self.preOrder(node.left);
			self.preOrder(node.right);
		}
	}

	self.debug = function(){
		self.preOrder(_root);
	}

	function searchRecursively(key, node){
		if (node === undefined || node.key == key){
			return node;
		}
		else if (key < node.key){
			return searchRecursively(key, node.left);
		}
		else {
			return searchRecursively(key, node.right);
		}
	}

	self.search = function(key){
		return searchRecursively(key, _root);
	}

	function removeRecursively(node, key){
		// Perform standard BST remove
		if (node === undefined){
			return node;
		}

		// If the key to be deleted is smaller than the node's key,
		// then it lies in the left subtree
		if (key < node.key){
			node.left = removeRecursively(node.left, key);
		}

		// If the key to be deleted is greater than the node's key,
		// then it lies in the right subtree
		if (key > node.key){
			node.right = removeRecursively(node.right, key);
		}

		// if key is same as node's key, then this is the node
		// TODO: what if same value???
		else {
			// node with only one child
		}
	}

	self.remove = function(key){
		_root = self.removeRecursively(_root, key);
	}

	return self;
}