import React from "react";
import Comment from "./components/Comment";
import CommentHeader from "./components/CommentHeader";
import Body from "./components/Body";
import data from "./data";

export default function App() {
  const comments = data.map((item) => {
    return <Comment key={item.id} item={item} />;
  });

  return (
    <div>
      <Body />
      <CommentHeader />
      <div>{comments}</div>
    </div>
  );
}
