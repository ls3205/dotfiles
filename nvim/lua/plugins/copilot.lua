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
			system_prompt = "You are a senior developer at a software consulting firm and your client has asked you a question. Please answer accordingly.\nFor any code that is written, it has been asked that you include as little comments as possible.\nThe question is as follows: ",
			model = "gpt-5.2-codex",
			chat_autocomplete = false,
			context = "#buffer:active",
		},
		-- See Commands section for default commands if you want to lazy load on them
	},
}
