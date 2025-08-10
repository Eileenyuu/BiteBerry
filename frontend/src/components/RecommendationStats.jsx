const RecommendationStats = ({ recommendationData }) => {
  if (!recommendationData?.has_ai_recommendations) {
    return null;
  }

  return (
    <div className="flex items-center justify-center gap-4 text-sm">
      <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-medium">
        🤖 {recommendationData.ai_count} AI-suggested
      </span>
      <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full font-medium">
        📋 {recommendationData.regular_count} filter-based
      </span>
    </div>
  );
};

export default RecommendationStats;