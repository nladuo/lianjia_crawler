
export const getDate = (timestamp) => {
  let newDate = new Date();
  newDate.setTime(timestamp * 1000);
  return newDate.toLocaleDateString();
}
