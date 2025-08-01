// Shared enum constants to prevent frontend-backend mismatches
// These values must match the backend Python enums exactly

export const DIETARY_RESTRICTIONS = {
  NONE: "none",
  VEGETARIAN: "vegetarian", 
  VEGAN: "vegan",
  GLUTEN_FREE: "gluten_free",
  DAIRY_FREE: "dairy_free",
  NUT_FREE: "nut_free",
  KETO: "keto",
  PALEO: "paleo"
};

export const DIFFICULTY_LEVELS = {
  EASY: "easy",
  MEDIUM: "medium", 
  HARD: "hard"
};

// Helper function to get dietary restriction options for dropdowns
export const getDietaryRestrictionOptions = () => [
  { value: DIETARY_RESTRICTIONS.NONE, label: "No dietary restrictions", emoji: "🍽️" },
  { value: DIETARY_RESTRICTIONS.VEGETARIAN, label: "Vegetarian", emoji: "🌱" },
  { value: DIETARY_RESTRICTIONS.VEGAN, label: "Vegan", emoji: "🌿" },
  { value: DIETARY_RESTRICTIONS.GLUTEN_FREE, label: "Gluten Free", emoji: "🌾" },
  { value: DIETARY_RESTRICTIONS.DAIRY_FREE, label: "Dairy Free", emoji: "🥛" },
  { value: DIETARY_RESTRICTIONS.NUT_FREE, label: "Nut Free", emoji: "🥜" },
  { value: DIETARY_RESTRICTIONS.KETO, label: "Keto", emoji: "🥩" },
  { value: DIETARY_RESTRICTIONS.PALEO, label: "Paleo", emoji: "🥩" }
];

// Helper function to validate dietary restriction values
export const isValidDietaryRestriction = (value) => {
  return Object.values(DIETARY_RESTRICTIONS).includes(value);
};

// Helper function to get difficulty level options for dropdowns
export const getDifficultyLevelOptions = () => [
  { value: DIFFICULTY_LEVELS.EASY, label: "Easy", emoji: "🟢" },
  { value: DIFFICULTY_LEVELS.MEDIUM, label: "Medium", emoji: "🟡" },
  { value: DIFFICULTY_LEVELS.HARD, label: "Hard", emoji: "🔴" }
];

// Helper function to validate difficulty level values
export const isValidDifficultyLevel = (value) => {
  return Object.values(DIFFICULTY_LEVELS).includes(value);
};