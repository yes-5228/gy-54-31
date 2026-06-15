const statusMap = {
  pending: "待处理",
  approved: "已通过",
  rejected: "已驳回",
};

export default function GradeTable({ grades, compact = false, onScoreChange }) {
  if (!grades.length) {
    return <div className="empty">暂无成绩记录</div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {!compact && <th>学号</th>}
            {!compact && <th>姓名</th>}
            <th>课程</th>
            <th>学期</th>
            <th>学分</th>
            <th>成绩</th>
            <th>绩点</th>
            <th>等级</th>
            <th>申诉</th>
          </tr>
        </thead>
        <tbody>
          {grades.map((grade) => (
            <tr key={grade.basic.id}>
              {!compact && <td>{grade.basic.student.studentNo}</td>}
              {!compact && <td>{grade.basic.student.name}</td>}
              <td>
                <strong>{grade.basic.courseName}</strong>
                <span>{grade.basic.courseCode}</span>
              </td>
              <td>{grade.basic.semester}</td>
              <td>{grade.basic.credit}</td>
              <td>
                {onScoreChange ? (
                  <input
                    className="score-input"
                    min="0"
                    max="100"
                    type="number"
                    value={grade.basic.score}
                    onChange={(event) => onScoreChange(grade.basic.id, event.target.value)}
                  />
                ) : (
                  grade.basic.score
                )}
              </td>
              <td>{grade.gpa.point.toFixed(1)}</td>
              <td>{grade.gpa.letter}</td>
              <td>
                {grade.appeal.status ? (
                  <span className={`status ${grade.appeal.status}`}>{statusMap[grade.appeal.status]}</span>
                ) : (
                  <span className="muted">无</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
