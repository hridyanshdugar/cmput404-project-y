import React, { createContext, useState } from "react";

export const PostContext = createContext<any[]>([]);

export const PostContextProvider = ({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) => {
	const [posts, setPosts] = useState<any | undefined>(undefined);
	const [replies, setReplies] = useState<any | undefined>(undefined);
	return (
		<PostContext.Provider value={[posts, setPosts, replies, setReplies]}>
			{children}
		</PostContext.Provider>
	);
};
