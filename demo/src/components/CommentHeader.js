import React from "react";
import data from "../data";
export default function CommentHeader() {
  return (
    <div className="header">
      <div className="header-bar">
        <div className="cmt-cnt-container">
          <div className="cmt-cnt-wrapper">
            <h4 className="header-black">回复</h4>
            <h4 className="cmt-cnt">{data.length}</h4>
          </div>
          <div className="cmt-indicator"></div>
        </div>
        <p className="header-grey">赞</p>
        <p className="header-grey">转发</p>
        <p className="header-grey">收藏</p>
      </div>
      <div className="header-down">全部回复</div>
    </div>
  );
}
