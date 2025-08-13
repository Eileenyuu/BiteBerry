import { useState } from "react";
import { toggleItem } from "../api/shopping";

const ShoppingListCard = ({ list, onDelete }) => {
  const [items, setItems] = useState(list.items || []);
  const [loading, setLoading] = useState(false);

  const handleToggleItem = async (itemId) => {
    setLoading(true);
    try {
      const response = await toggleItem(itemId);
      // Update the item in local state
      setItems(
        items.map((item) =>
          item.id === itemId
            ? { ...item, is_checked: response.is_checked }
            : item
        )
      );
    } catch (error) {
      console.error("Error toggling item:", error);
      alert("Failed to update item");
    } finally {
      setLoading(false);
    }
  };

  const checkedCount = items.filter((item) => item.is_checked).length;
  const totalCount = items.length;

  // Separate unchecked and checked items
  const uncheckedItems = items.filter((item) => !item.is_checked);
  const checkedItems = items.filter((item) => item.is_checked);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl text-left font-semibold text-gray-900">
            {list.name}
          </h3>
          <p className="text-sm text-gray-500">
            {checkedCount} of {totalCount} items completed
          </p>
        </div>
        <button
          onClick={onDelete}
          className="text-red-500 hover:text-red-700 text-sm font-medium"
        >
          Delete
        </button>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
        <div
          className="bg-green-500 h-2 rounded-full transition-all duration-300"
          style={{
            width:
              totalCount > 0 ? `${(checkedCount / totalCount) * 100}%` : "0%",
          }}
        ></div>
      </div>

      {/* Items List */}
      <div className="space-y-2">
        {items.length === 0 ? (
          <p className="text-gray-500 text-sm">No items in this list</p>
        ) : (
          <>
            {/* Unchecked Items */}
            {uncheckedItems.map((item) => (
              <div key={item.id} className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={item.is_checked}
                  onChange={() => handleToggleItem(item.id)}
                  disabled={loading}
                  className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                />
                <span className="flex-1 text-gray-900">
                  {item.quantity} {item.ingredient}
                </span>
              </div>
            ))}

            {/* Separator if there are both unchecked and checked items */}
            {uncheckedItems.length > 0 && checkedItems.length > 0 && (
              <div className="border-t border-gray-200 my-3"></div>
            )}

            {/* Checked Items */}
            {checkedItems.map((item) => (
              <div key={item.id} className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={item.is_checked}
                  onChange={() => handleToggleItem(item.id)}
                  disabled={loading}
                  className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                />
                <span className="flex-1 text-gray-500 line-through">
                  {item.quantity} {item.ingredient}
                </span>
              </div>
            ))}
          </>
        )}
      </div>

      {/* Created Date */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-400">
          Created: {new Date(list.created_at).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
};

export default ShoppingListCard;
