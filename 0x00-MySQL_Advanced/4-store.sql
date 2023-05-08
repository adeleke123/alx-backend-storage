-- Script creates a trigger that decreases the quantity of an item after adding
-- a new order and Quantity can be negative.

CREATE TRIGGER decrease_quant AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
