// filepath: /home/insantaqwa/Documents/coding/api tb40/api-tb40/utils/coloring.js
function scoreToColor(score) {
  // Ensure score is between 0 and 100
  score = Math.max(0, Math.min(100, score));
  
  let startColor, endColor, interpolationFactor;
  
  // Determine color interpolation based on score
  if (score <= 50) {
    startColor = [191, 64, 64]; // Red (#bf4040)
    endColor = [64, 191, 64];   // Green (#40bf40)
    interpolationFactor = score / 50;
  } else {
    startColor = [64, 191, 64]; // Green (#40bf40)
    endColor = [64, 64, 191];   // Blue (#4040bf)
    interpolationFactor = (score - 50) / 50;
  }
  
  // Interpolate between colors
  const interpolatedColor = startColor.map((channel, i) => 
    Math.round(channel + (endColor[i] - channel) * interpolationFactor)
  );
  
  // Convert to hex with fixed 50% saturation
  return `#${interpolatedColor.map(c => c.toString(16).padStart(2, '0')).join('')}`;
}

function rankToColor(rank, lowestRank) {
  // Ensure rank is within valid range
  rank = Math.max(1, Math.min(rank, lowestRank));
  
  // Calculate normalized score (0-100)
  const score = ((lowestRank - rank) / (lowestRank - 1)) * 100;
  
  // Reuse previous scoreToColor logic
  return scoreToColor(score);
}

module.exports = { scoreToColor, rankToColor };