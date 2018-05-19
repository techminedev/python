from orator.migrations import Migration


class CreateTasksTable(Migration):

	def up(self):
		"""
		Run the migrations.
		"""
		with self.schema.create('tasks') as table:
			table.increments('id')
			table.string("task_id")
			table.long_text("target_url")
			table.long_text("image_url")
			table.string("image_path").default("")
			table.integer("screen_width").unsigned().default(0)
			table.integer("screen_height").unsigned().default(0)
			table.integer("status").unsigned().default(0)
			table.integer("processing_status").unsigned().default(0)
			table.timestamps()

	def down(self):
		"""
		Revert the migrations.
		"""
		self.schema.drop('tasks')
