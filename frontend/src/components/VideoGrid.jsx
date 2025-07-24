import VideoCard from "./VideoCard";

const VideoGrid = ({videos}) => {
  return (
    <div className="gap-x-[30px] gap-y-[30px] px-[100px] mt-10 max-w-8xl grid grid-cols-2 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3">
      {videos.map((video) => (
        <VideoCard
          key={video.id}
          title={video.title}
          thumbnail={`http://localhost:5000${video.thumbnail}`}
          filename={video.filename}
        />
      ))}
    </div>
  );
};

export default VideoGrid;
