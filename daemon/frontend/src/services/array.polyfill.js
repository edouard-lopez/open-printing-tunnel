// Get the index of the object inside an array, matching a condition
// @see: http://stackoverflow.com/a/15998003/802365
if (!Array.prototype.getIndex) {
	Array.prototype.findIndex = function (predicate) {
		'use strict';
		if (this == null) {
			throw new TypeError('Array.prototype.findIndex called on null or undefined');
		}
		if (typeof predicate !== 'function') {
			throw new TypeError('predicate must be a function');
		}
		var list = Object(this);
		var length = list.length >>> 0;
		var thisArg = arguments[1];
		var value;

		for (var i = 0; i < length; i++) {
			value = list[i];
			if (predicate.call(thisArg, value, i, list)) {
				return i;
			}
		}
		return -1;
	};
}


/*
 * check if an element exists in array using a comparer function
 * comparer : function(currentElement)
 * @see: http://stackoverflow.com/a/1988361/802365
 */
Array.prototype.inArray = function (comparer) {
	for (var i = 0; i < this.length; i++) {
		if (comparer(this[i])) {
			return true;
		}
	}
	return false;
};

/*
 * adds an element to the array if it does not already exist using a comparer function
 * @see: http://stackoverflow.com/a/1988361/802365
 */
Array.prototype.pushIfNotInArray = function (element, comparer) {
	if (!this.inArray(comparer)) {
		this.push(element);
	}
};


/*
 * Remove an item or interval of items from array
 * @see: http://stackoverflow.com/a/9815010/802365
 */
Array.prototype.remove = function (from, to) {
	var rest = this.slice((to || from) + 1 || this.length);
	this.length = from < 0 ? this.length + from : from;
	return this.push.apply(this, rest);
};

/* Polyfill: Array.prototype.find()
 see: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/find
 */
if (!Array.prototype.find) {
	Array.prototype.find = function (predicate) {
		if (this == null) {
			throw new TypeError('Array.prototype.find called on null or undefined');
		}
		if (typeof predicate !== 'function') {
			throw new TypeError('predicate must be a function');
		}
		var list = Object(this);
		var length = list.length >>> 0;
		var thisArg = arguments[1];
		var value;

		for (var i = 0; i < length; i++) {
			value = list[i];
			if (predicate.call(thisArg, value, i, list)) {
				return value;
			}
		}
		return undefined;
	};
}
