const VideoCard = ({ title, thumbnail, filename }) => {
  return (
      <div className="rounded-lg overflow-hidden">
        <img
          src={thumbnail}
          alt={title}
          className="w-full aspect-video object-cover rounded-lg"
        />
        <div className="p-2">
          <div className="text-sm font-medium text-black line-clamp-2">
            {title}
          </div>
        </div>
      </div>
  );
};

export default VideoCard;
