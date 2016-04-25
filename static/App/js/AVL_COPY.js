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

	self.rightRotate = function(y){
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

	self.leftRotate = function(x){
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
		return self.height(node.left) - self.height(node.right);
	}

	function insertRecursively(node, key, data, parent, direction){
		// Perform the normal BST rotation
		if (node === undefined){
			var newNode = Node(key, data);
			if (parent === undefined){
				_root = newNode;	
			}
			else {
				if (direction == LEFT_DIRECTION){
					parent.left = newNode;
				}
				else {
					parent.right = newNode;
				}
			}
		}
		else if (key < node.key){
			insertRecursively(node.left, key, data, node, LEFT_DIRECTION);
		}
		else {
			insertRecursively(node.right, key, data, node, RIGHT_DIRECTION);
		}

		// Update height of this ancestor node
		node.height = Math.max(height(node.left), height(node.right)) + 1;

		// Get the balance factor of this ancestor node to check whether
		// this node became unbalanced
		var balance = getBalance(node);
	}

	self.insert = function(key, data){
		insertRecursively(_root, key, data, undefined, 0);
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

	self.remove = function(key){
		// TODO
	}

	function rotate(){
		// TODO
	}

	return self;
}