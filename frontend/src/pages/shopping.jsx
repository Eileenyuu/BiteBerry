import { useState, useEffect } from "react";
import {
  getShoppingLists,
  createShoppingList,
  deleteShoppingList,
} from "../api/shopping";
import { getUserLikedRecipes } from "../api/likes";
import ShoppingListCard from "../components/ShoppingListCard";

const Shopping = ({ user }) => {
  const [shoppingLists, setShoppingLists] = useState([]);
  const [selectedRecipes, setSelectedRecipes] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newListName, setNewListName] = useState("");
  const [loading, setLoading] = useState(false);
  const [deleteModal, setDeleteModal] = useState({
    show: false,
    listId: null,
    listName: "",
  });

  // Load shopping lists and recipes on component mount
  useEffect(() => {
    if (user?.id) {
      fetchShoppingLists();
      fetchRecipes();
    }
  }, [user]);

  const fetchShoppingLists = async () => {
    try {
      const lists = await getShoppingLists(user.id);
      setShoppingLists(lists);
    } catch (error) {
      console.error("Error fetching shopping lists:", error);
    }
  };

  const fetchRecipes = async () => {
    try {
      const likedRecipes = await getUserLikedRecipes(user.id);
      setRecipes(likedRecipes);
    } catch (error) {
      console.error("Error fetching liked recipes:", error);
    }
  };

  const handleCreateList = async (e) => {
    e.preventDefault();

    if (!newListName || selectedRecipes.length === 0) {
      alert("Please enter a name and select at least one recipe");
      return;
    }

    setLoading(true);
    try {
      const newList = await createShoppingList(user.id, {
        name: newListName,
        recipe_ids: selectedRecipes,
      });

      setShoppingLists([...shoppingLists, newList]);
      setNewListName("");
      setSelectedRecipes([]);
      setShowCreateForm(false);
    } catch (error) {
      console.error("Error creating shopping list:", error);
      alert("Failed to create shopping list");
    } finally {
      setLoading(false);
    }
  };

  const handleRecipeSelect = (recipeId) => {
    if (selectedRecipes.includes(recipeId)) {
      setSelectedRecipes(selectedRecipes.filter((id) => id !== recipeId));
    } else {
      setSelectedRecipes([...selectedRecipes, recipeId]);
    }
  };

  const handleDeleteList = (listId, listName) => {
    setDeleteModal({ show: true, listId, listName });
  };

  const confirmDelete = async () => {
    try {
      await deleteShoppingList(deleteModal.listId, user.id);
      setShoppingLists(
        shoppingLists.filter((list) => list.id !== deleteModal.listId)
      );
      setDeleteModal({ show: false, listId: null, listName: "" });
    } catch (error) {
      console.error("Error deleting shopping list:", error);
      alert("Failed to delete shopping list");
    }
  };

  const cancelDelete = () => {
    setDeleteModal({ show: false, listId: null, listName: "" });
  };

  return (
    <div className="min-h-screen w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🛒 Shopping Lists
          </h1>
          <p className="text-lg text-gray-600">
            Create shopping lists from your liked recipes
          </p>
        </div>

        {/* Create List Button */}
        <div className="mb-8 text-center">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            {showCreateForm ? "Cancel" : "Create New List"}
          </button>
        </div>

        {/* Create Form */}
        {showCreateForm && (
          <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <form onSubmit={handleCreateList}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  List Name
                </label>
                <input
                  type="text"
                  value={newListName}
                  onChange={(e) => setNewListName(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:ring-red-500 focus:border-red-500"
                  placeholder="e.g., Weekly Groceries"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Recipes ({selectedRecipes.length} selected)
                </label>
                <div className="max-h-60 overflow-y-auto border border-gray-300 rounded-md p-2">
                  {recipes.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-gray-500 mb-2">
                        No liked recipes found
                      </p>
                      <p className="text-sm text-gray-400">
                        Go to "All Recipes" or "Preferences" to like some
                        recipes first!
                      </p>
                    </div>
                  ) : (
                    recipes.map((recipe) => (
                      <label
                        key={recipe.id}
                        className="flex items-center p-2 hover:bg-gray-50 cursor-pointer"
                      >
                        <input
                          type="checkbox"
                          checked={selectedRecipes.includes(recipe.id)}
                          onChange={() => handleRecipeSelect(recipe.id)}
                          className="mr-3"
                        />
                        <span className="text-sm">{recipe.title}</span>
                      </label>
                    ))
                  )}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md font-medium disabled:opacity-50 transition-colors"
              >
                {loading ? "Creating..." : "Create List"}
              </button>
            </form>
          </div>
        )}

        {/* Shopping Lists */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {shoppingLists.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <p className="text-gray-500 text-lg">No shopping lists yet</p>
              <p className="text-gray-400">
                Create your first list to get started!
              </p>
            </div>
          ) : (
            shoppingLists.map((list) => (
              <ShoppingListCard
                key={list.id}
                list={list}
                onDelete={() => handleDeleteList(list.id, list.name)}
              />
            ))
          )}
        </div>

        {/* Delete Confirmation Modal */}
        {deleteModal.show && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Delete Shopping List
              </h3>
              <p className="text-gray-600 mb-6">
                Are you sure you want to delete "{deleteModal.listName}"? This
                action cannot be undone.
              </p>
              <div className="flex justify-end space-x-3">
                <button
                  onClick={cancelDelete}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmDelete}
                  className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Shopping;
