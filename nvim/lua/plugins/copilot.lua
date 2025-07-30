return {
	{
		"CopilotC-Nvim/CopilotChat.nvim",
		dependencies = {
			-- {
			-- 	"github/copilot.vim",
			-- 	init = function()
			-- 		vim.g.copilot_no_tab_map = true
			-- 	end,
			-- }, -- or zbirenbaum/copilot.lua
			{ "zbirenbaum/copilot.lua" },
			{ "nvim-lua/plenary.nvim", branch = "master" }, -- for curl, log and async functions
		},
		build = "make tiktoken", -- Only on MacOS or Linux
		opts = {
			model = "claude-sonnet-4",
			chat_autocomplete = false,
			context = "#buffers:visible",
		},
		-- See Commands section for default commands if you want to lazy load on them
	},
}
