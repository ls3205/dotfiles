return {
	-- {
	-- 	"craftzdog/solarized-osaka.nvim",
	-- 	lazy = true,
	-- 	priority = 1000,
	-- 	opts = function()
	-- 		return {
	-- 			transparent = true,
	-- 		}
	-- 	end,
	-- },
	{
		"folke/tokyonight.nvim",
		lazy = false,
		priority = 1000,
		opts = {
			style = "storm",
			transparent = true,
			styles = {
				comments = { italic = false },
				keywords = { italic = false },
			},
		},
	},
}
